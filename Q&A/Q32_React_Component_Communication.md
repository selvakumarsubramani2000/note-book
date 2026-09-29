# Question 32: How do you communicate between components in React?

## Answer

React components communicate through several patterns. Let me explain each with examples.

---

## 1. Parent to Child - Props (Most Common)

**Pass data down using props**

```jsx
// Parent Component
function ProductList() {
  const products = [
    { id: 1, name: 'Laptop', price: 999 },
    { id: 2, name: 'Mouse', price: 29 }
  ];
  
  return (
    <div>
      {products.map(product => (
        <ProductCard 
          key={product.id}
          product={product}
          discount={10}
        />
      ))}
    </div>
  );
}

// Child Component
function ProductCard({ product, discount }) {
  const finalPrice = product.price - (product.price * discount / 100);
  
  return (
    <div className="card">
      <h3>{product.name}</h3>
      <p>Price: ${product.price}</p>
      <p>Discounted: ${finalPrice}</p>
    </div>
  );
}
```

---

## 2. Child to Parent - Callback Functions

**Pass functions as props to send data up**

```jsx
// Parent Component
function ShoppingCart() {
  const [cartItems, setCartItems] = useState([]);
  
  // Callback function
  const handleAddToCart = (product) => {
    setCartItems([...cartItems, product]);
    console.log('Added to cart:', product);
  };
  
  const handleRemoveFromCart = (productId) => {
    setCartItems(cartItems.filter(item => item.id !== productId));
  };
  
  return (
    <div>
      <ProductList onAddToCart={handleAddToCart} />
      <Cart 
        items={cartItems} 
        onRemoveItem={handleRemoveFromCart} 
      />
    </div>
  );
}

// Child Component
function ProductList({ onAddToCart }) {
  const products = [
    { id: 1, name: 'Laptop', price: 999 },
    { id: 2, name: 'Mouse', price: 29 }
  ];
  
  return (
    <div>
      {products.map(product => (
        <div key={product.id}>
          <h3>{product.name}</h3>
          <button onClick={() => onAddToCart(product)}>
            Add to Cart
          </button>
        </div>
      ))}
    </div>
  );
}

// Another Child
function Cart({ items, onRemoveItem }) {
  return (
    <div>
      <h2>Cart ({items.length})</h2>
      {items.map(item => (
        <div key={item.id}>
          <span>{item.name}</span>
          <button onClick={() => onRemoveItem(item.id)}>Remove</button>
        </div>
      ))}
    </div>
  );
}
```

---

## 3. Sibling to Sibling - Lift State Up

**Move shared state to common parent**

```jsx
function App() {
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');
  
  return (
    <div>
      {/* Sibling 1 */}
      <FilterBar 
        onCategoryChange={setSelectedCategory}
        onSearchChange={setSearchTerm}
      />
      
      {/* Sibling 2 */}
      <ProductGrid 
        category={selectedCategory}
        search={searchTerm}
      />
    </div>
  );
}

// Sibling 1
function FilterBar({ onCategoryChange, onSearchChange }) {
  return (
    <div>
      <select onChange={(e) => onCategoryChange(e.target.value)}>
        <option value="all">All</option>
        <option value="electronics">Electronics</option>
        <option value="clothing">Clothing</option>
      </select>
      
      <input 
        type="text"
        placeholder="Search..."
        onChange={(e) => onSearchChange(e.target.value)}
      />
    </div>
  );
}

// Sibling 2
function ProductGrid({ category, search }) {
  const [products] = useState([/* products */]);
  
  const filtered = products.filter(p => 
    (category === 'all' || p.category === category) &&
    p.name.toLowerCase().includes(search.toLowerCase())
  );
  
  return (
    <div>
      {filtered.map(p => <ProductCard key={p.id} product={p} />)}
    </div>
  );
}
```

---

## 4. Context API - Global State (Any to Any)

**Share data across component tree without prop drilling**

```jsx
import { createContext, useContext, useState } from 'react';

// 1. Create Context
const UserContext = createContext();

// 2. Create Provider Component
function UserProvider({ children }) {
  const [user, setUser] = useState(null);
  
  const login = (userData) => {
    setUser(userData);
  };
  
  const logout = () => {
    setUser(null);
  };
  
  return (
    <UserContext.Provider value={{ user, login, logout }}>
      {children}
    </UserContext.Provider>
  );
}

// 3. Custom Hook for easy access
function useUser() {
  const context = useContext(UserContext);
  if (!context) {
    throw new Error('useUser must be used within UserProvider');
  }
  return context;
}

// 4. Wrap App with Provider
function App() {
  return (
    <UserProvider>
      <Header />
      <Dashboard />
      <Footer />
    </UserProvider>
  );
}

// 5. Use in any component (no prop drilling!)
function Header() {
  const { user, logout } = useUser();
  
  return (
    <header>
      {user ? (
        <>
          <span>Welcome, {user.name}</span>
          <button onClick={logout}>Logout</button>
        </>
      ) : (
        <LoginButton />
      )}
    </header>
  );
}

function Dashboard() {
  const { user } = useUser();
  
  if (!user) {
    return <div>Please login</div>;
  }
  
  return <div>Dashboard for {user.name}</div>;
}

function LoginButton() {
  const { login } = useUser();
  
  const handleLogin = () => {
    login({ id: 1, name: 'John Doe', email: 'john@example.com' });
  };
  
  return <button onClick={handleLogin}>Login</button>;
}
```

---

## 5. Custom Hooks - Reusable Logic

**Share logic between components**

```jsx
// Custom hook for form handling
function useForm(initialValues) {
  const [values, setValues] = useState(initialValues);
  
  const handleChange = (e) => {
    setValues({
      ...values,
      [e.target.name]: e.target.value
    });
  };
  
  const reset = () => {
    setValues(initialValues);
  };
  
  return { values, handleChange, reset };
}

// Use in multiple components
function LoginForm() {
  const { values, handleChange, reset } = useForm({
    email: '',
    password: ''
  });
  
  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Login:', values);
    reset();
  };
  
  return (
    <form onSubmit={handleSubmit}>
      <input name="email" value={values.email} onChange={handleChange} />
      <input name="password" type="password" value={values.password} onChange={handleChange} />
      <button type="submit">Login</button>
    </form>
  );
}

function RegisterForm() {
  const { values, handleChange } = useForm({
    name: '',
    email: '',
    password: ''
  });
  
  return (
    <form>
      <input name="name" value={values.name} onChange={handleChange} />
      <input name="email" value={values.email} onChange={handleChange} />
      <input name="password" type="password" value={values.password} onChange={handleChange} />
    </form>
  );
}
```

---

## 6. Event Bus / PubSub Pattern (Rare)

**Use external library for unrelated components**

```jsx
// Using a simple event emitter
import EventEmitter from 'events';

const eventBus = new EventEmitter();

// Component 1 - Emits event
function ProductPage() {
  const addToCart = (product) => {
    eventBus.emit('addToCart', product);
  };
  
  return (
    <button onClick={() => addToCart({ id: 1, name: 'Laptop' })}>
      Add to Cart
    </button>
  );
}

// Component 2 - Listens to event (unrelated component)
function CartBadge() {
  const [count, setCount] = useState(0);
  
  useEffect(() => {
    const handler = () => {
      setCount(c => c + 1);
    };
    
    eventBus.on('addToCart', handler);
    
    return () => {
      eventBus.off('addToCart', handler);
    };
  }, []);
  
  return <div>Cart ({count})</div>;
}
```

---

## Real-World Example: E-Commerce App

```jsx
import { createContext, useContext, useState, useEffect } from 'react';

// Context for cart management
const CartContext = createContext();

function CartProvider({ children }) {
  const [items, setItems] = useState([]);
  
  const addItem = (product) => {
    setItems(prev => {
      const existing = prev.find(item => item.id === product.id);
      if (existing) {
        return prev.map(item =>
          item.id === product.id
            ? { ...item, quantity: item.quantity + 1 }
            : item
        );
      }
      return [...prev, { ...product, quantity: 1 }];
    });
  };
  
  const removeItem = (productId) => {
    setItems(prev => prev.filter(item => item.id !== productId));
  };
  
  const updateQuantity = (productId, quantity) => {
    setItems(prev =>
      prev.map(item =>
        item.id === productId ? { ...item, quantity } : item
      )
    );
  };
  
  const total = items.reduce((sum, item) => sum + (item.price * item.quantity), 0);
  
  return (
    <CartContext.Provider value={{ items, addItem, removeItem, updateQuantity, total }}>
      {children}
    </CartContext.Provider>
  );
}

function useCart() {
  return useContext(CartContext);
}

// App structure
function App() {
  return (
    <CartProvider>
      <Header />
      <main>
        <ProductList />
        <CartSidebar />
      </main>
    </CartProvider>
  );
}

// Header shows cart count
function Header() {
  const { items } = useCart();
  const itemCount = items.reduce((sum, item) => sum + item.quantity, 0);
  
  return (
    <header>
      <h1>My Store</h1>
      <div>Cart ({itemCount})</div>
    </header>
  );
}

// Product list adds items
function ProductList() {
  const { addItem } = useCart();
  const products = [
    { id: 1, name: 'Laptop', price: 999 },
    { id: 2, name: 'Mouse', price: 29 }
  ];
  
  return (
    <div>
      {products.map(product => (
        <div key={product.id}>
          <h3>{product.name}</h3>
          <p>${product.price}</p>
          <button onClick={() => addItem(product)}>Add to Cart</button>
        </div>
      ))}
    </div>
  );
}

// Cart sidebar shows items
function CartSidebar() {
  const { items, removeItem, updateQuantity, total } = useCart();
  
  return (
    <div className="cart-sidebar">
      <h2>Shopping Cart</h2>
      {items.map(item => (
        <div key={item.id}>
          <span>{item.name}</span>
          <input 
            type="number"
            value={item.quantity}
            onChange={(e) => updateQuantity(item.id, parseInt(e.target.value))}
          />
          <span>${item.price * item.quantity}</span>
          <button onClick={() => removeItem(item.id)}>Remove</button>
        </div>
      ))}
      <div>Total: ${total.toFixed(2)}</div>
    </div>
  );
}
```

---

## Communication Patterns Summary

| Pattern | Direction | Use Case | Performance |
|---------|-----------|----------|-------------|
| **Props** | Parent → Child | Simple data passing | ✅ Fast |
| **Callbacks** | Child → Parent | Events, actions | ✅ Fast |
| **Lift State** | Sibling ↔ Sibling | Shared state | ✅ Fast |
| **Context** | Any ↔ Any | Global state | 🟡 Moderate |
| **Custom Hooks** | Any ↔ Any | Reusable logic | ✅ Fast |
| **Redux** | Any ↔ Any | Complex global state | 🟡 Moderate |

---

## Best Practices

1. ✅ **Use props for simple parent-child** communication
2. ✅ **Use Context for global state** (theme, auth, cart)
3. ✅ **Lift state up** only when necessary
4. ✅ **Custom hooks** for reusable logic
5. ✅ **Keep Context focused** (separate contexts for different concerns)
6. ❌ **Don't overuse Context** (performance impact if too many consumers)
7. ❌ **Don't prop drill** more than 2-3 levels (use Context instead)

---

## Common Mistakes

```jsx
// ❌ BAD - Prop drilling too deep
<App>
  <Header user={user}>
    <Nav user={user}>
      <UserMenu user={user} />  // Too many levels!
    </Nav>
  </Header>
</App>

// ✅ GOOD - Use Context
<UserProvider>
  <App>
    <Header>
      <Nav>
        <UserMenu />  // Gets user from context
      </Nav>
    </Header>
  </App>
</UserProvider>
```

---

## Summary

**Component Communication Methods:**
1. **Props** - Parent to child
2. **Callbacks** - Child to parent
3. **Lift State** - Sibling to sibling
4. **Context** - Global state
5. **Custom Hooks** - Shared logic

Choose based on relationship between components and data flow needs!
