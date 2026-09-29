# Question 30: How do you handle state management in React?

## Answer

### What is State in React?

**State** is data that changes over time in your component. When state changes, React re-renders the component to reflect the new data.

---

## 1. Local Component State (useState)

### Basic Usage

```jsx
import React, { useState } from 'react';

function Counter() {
    // Declare state variable
    const [count, setCount] = useState(0); // Initial value: 0
    
    return (
        <div>
            <p>Count: {count}</p>
            <button onClick={() => setCount(count + 1)}>Increment</button>
            <button onClick={() => setCount(count - 1)}>Decrement</button>
            <button onClick={() => setCount(0)}>Reset</button>
        </div>
    );
}
```

### Multiple State Variables

```jsx
function UserForm() {
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [age, setAge] = useState(0);
    
    const handleSubmit = (e) => {
        e.preventDefault();
        console.log({ name, email, age });
    };
    
    return (
        <form onSubmit={handleSubmit}>
            <input 
                value={name} 
                onChange={(e) => setName(e.target.value)} 
                placeholder="Name" 
            />
            <input 
                value={email} 
                onChange={(e) => setEmail(e.target.value)} 
                placeholder="Email" 
            />
            <input 
                type="number"
                value={age} 
                onChange={(e) => setAge(parseInt(e.target.value))} 
                placeholder="Age" 
            />
            <button type="submit">Submit</button>
        </form>
    );
}
```

### State with Objects

```jsx
function UserProfile() {
    const [user, setUser] = useState({
        name: '',
        email: '',
        address: {
            street: '',
            city: '',
            zipCode: ''
        }
    });
    
    const handleChange = (e) => {
        const { name, value } = e.target;
        setUser(prev => ({
            ...prev,
            [name]: value
        }));
    };
    
    const handleAddressChange = (e) => {
        const { name, value } = e.target;
        setUser(prev => ({
            ...prev,
            address: {
                ...prev.address,
                [name]: value
            }
        }));
    };
    
    return (
        <div>
            <input name="name" value={user.name} onChange={handleChange} />
            <input name="email" value={user.email} onChange={handleChange} />
            <input name="street" value={user.address.street} onChange={handleAddressChange} />
            <input name="city" value={user.address.city} onChange={handleAddressChange} />
        </div>
    );
}
```

---

## 2. Prop Drilling (Passing State Down)

```jsx
// Parent Component
function App() {
    const [user, setUser] = useState({ name: 'John', role: 'Admin' });
    
    return (
        <div>
            <Header user={user} />
            <Dashboard user={user} setUser={setUser} />
        </div>
    );
}

// Child Component
function Header({ user }) {
    return <h1>Welcome, {user.name}</h1>;
}

// Grandchild Component
function Dashboard({ user, setUser }) {
    return (
        <div>
            <UserProfile user={user} setUser={setUser} />
        </div>
    );
}

function UserProfile({ user, setUser }) {
    const updateRole = () => {
        setUser(prev => ({ ...prev, role: 'User' }));
    };
    
    return (
        <div>
            <p>Role: {user.role}</p>
            <button onClick={updateRole}>Change Role</button>
        </div>
    );
}
```

**Problem**: Props need to be passed through many levels (prop drilling)

---

## 3. Context API (Global State)

### Creating and Using Context

```jsx
import React, { createContext, useContext, useState } from 'react';

// 1. Create Context
const UserContext = createContext();

// 2. Create Provider Component
function UserProvider({ children }) {
    const [user, setUser] = useState({
        name: 'John Doe',
        email: 'john@example.com',
        role: 'Admin'
    });
    
    const updateUser = (updates) => {
        setUser(prev => ({ ...prev, ...updates }));
    };
    
    const logout = () => {
        setUser(null);
    };
    
    return (
        <UserContext.Provider value={{ user, updateUser, logout }}>
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

// 4. Use in App
function App() {
    return (
        <UserProvider>
            <Header />
            <Dashboard />
            <Settings />
        </UserProvider>
    );
}

// 5. Access context in any component (no prop drilling!)
function Header() {
    const { user } = useUser();
    return <h1>Welcome, {user?.name}</h1>;
}

function Settings() {
    const { user, updateUser, logout } = useUser();
    
    return (
        <div>
            <p>Email: {user?.email}</p>
            <button onClick={() => updateUser({ role: 'User' })}>
                Change Role
            </button>
            <button onClick={logout}>Logout</button>
        </div>
    );
}
```

---

## 4. useReducer (Complex State Logic)

```jsx
import React, { useReducer } from 'react';

// 1. Define initial state
const initialState = {
    cart: [],
    total: 0
};

// 2. Define reducer function
function cartReducer(state, action) {
    switch (action.type) {
        case 'ADD_ITEM':
            return {
                ...state,
                cart: [...state.cart, action.payload],
                total: state.total + action.payload.price
            };
        
        case 'REMOVE_ITEM':
            const itemToRemove = state.cart.find(item => item.id === action.payload);
            return {
                ...state,
                cart: state.cart.filter(item => item.id !== action.payload),
                total: state.total - itemToRemove.price
            };
        
        case 'CLEAR_CART':
            return initialState;
        
        case 'UPDATE_QUANTITY':
            return {
                ...state,
                cart: state.cart.map(item =>
                    item.id === action.payload.id
                        ? { ...item, quantity: action.payload.quantity }
                        : item
                )
            };
        
        default:
            return state;
    }
}

// 3. Use in component
function ShoppingCart() {
    const [state, dispatch] = useReducer(cartReducer, initialState);
    
    const addItem = (item) => {
        dispatch({ type: 'ADD_ITEM', payload: item });
    };
    
    const removeItem = (id) => {
        dispatch({ type: 'REMOVE_ITEM', payload: id });
    };
    
    const clearCart = () => {
        dispatch({ type: 'CLEAR_CART' });
    };
    
    return (
        <div>
            <h2>Shopping Cart</h2>
            {state.cart.map(item => (
                <div key={item.id}>
                    <span>{item.name} - ${item.price}</span>
                    <button onClick={() => removeItem(item.id)}>Remove</button>
                </div>
            ))}
            <h3>Total: ${state.total}</h3>
            <button onClick={clearCart}>Clear Cart</button>
        </div>
    );
}
```

---

## 5. Redux (Large Applications)

### Installation
```bash
npm install @reduxjs/toolkit react-redux
```

### Redux Setup

```jsx
// store.js
import { configureStore, createSlice } from '@reduxjs/toolkit';

// 1. Create slice
const userSlice = createSlice({
    name: 'user',
    initialState: {
        currentUser: null,
        isAuthenticated: false
    },
    reducers: {
        loginUser: (state, action) => {
            state.currentUser = action.payload;
            state.isAuthenticated = true;
        },
        logoutUser: (state) => {
            state.currentUser = null;
            state.isAuthenticated = false;
        },
        updateUser: (state, action) => {
            state.currentUser = { ...state.currentUser, ...action.payload };
        }
    }
});

export const { loginUser, logoutUser, updateUser } = userSlice.actions;

// 2. Create store
export const store = configureStore({
    reducer: {
        user: userSlice.reducer
    }
});

// App.jsx
import { Provider } from 'react-redux';
import { store } from './store';

function App() {
    return (
        <Provider store={store}>
            <Dashboard />
        </Provider>
    );
}

// Component using Redux
import { useSelector, useDispatch } from 'react-redux';
import { loginUser, logoutUser } from './store';

function Dashboard() {
    const user = useSelector(state => state.user.currentUser);
    const isAuthenticated = useSelector(state => state.user.isAuthenticated);
    const dispatch = useDispatch();
    
    const handleLogin = () => {
        dispatch(loginUser({ 
            name: 'John Doe', 
            email: 'john@example.com' 
        }));
    };
    
    const handleLogout = () => {
        dispatch(logoutUser());
    };
    
    return (
        <div>
            {isAuthenticated ? (
                <>
                    <h1>Welcome, {user.name}</h1>
                    <button onClick={handleLogout}>Logout</button>
                </>
            ) : (
                <button onClick={handleLogin}>Login</button>
            )}
        </div>
    );
}
```

---

## 6. Real-World Example: E-Commerce App

```jsx
import React, { createContext, useContext, useReducer } from 'react';

// Context
const AppContext = createContext();

// Initial State
const initialState = {
    products: [],
    cart: [],
    user: null,
    loading: false,
    error: null
};

// Reducer
function appReducer(state, action) {
    switch (action.type) {
        case 'SET_PRODUCTS':
            return { ...state, products: action.payload, loading: false };
        
        case 'ADD_TO_CART':
            const existingItem = state.cart.find(item => item.id === action.payload.id);
            if (existingItem) {
                return {
                    ...state,
                    cart: state.cart.map(item =>
                        item.id === action.payload.id
                            ? { ...item, quantity: item.quantity + 1 }
                            : item
                    )
                };
            }
            return {
                ...state,
                cart: [...state.cart, { ...action.payload, quantity: 1 }]
            };
        
        case 'REMOVE_FROM_CART':
            return {
                ...state,
                cart: state.cart.filter(item => item.id !== action.payload)
            };
        
        case 'SET_USER':
            return { ...state, user: action.payload };
        
        case 'SET_LOADING':
            return { ...state, loading: action.payload };
        
        case 'SET_ERROR':
            return { ...state, error: action.payload, loading: false };
        
        default:
            return state;
    }
}

// Provider
export function AppProvider({ children }) {
    const [state, dispatch] = useReducer(appReducer, initialState);
    
    return (
        <AppContext.Provider value={{ state, dispatch }}>
            {children}
        </AppContext.Provider>
    );
}

// Hook
export function useApp() {
    return useContext(AppContext);
}

// Usage in component
function ProductList() {
    const { state, dispatch } = useApp();
    
    useEffect(() => {
        fetchProducts();
    }, []);
    
    const fetchProducts = async () => {
        dispatch({ type: 'SET_LOADING', payload: true });
        try {
            const response = await fetch('/api/products');
            const data = await response.json();
            dispatch({ type: 'SET_PRODUCTS', payload: data });
        } catch (error) {
            dispatch({ type: 'SET_ERROR', payload: error.message });
        }
    };
    
    const addToCart = (product) => {
        dispatch({ type: 'ADD_TO_CART', payload: product });
    };
    
    if (state.loading) return <div>Loading...</div>;
    if (state.error) return <div>Error: {state.error}</div>;
    
    return (
        <div>
            {state.products.map(product => (
                <div key={product.id}>
                    <h3>{product.name}</h3>
                    <p>${product.price}</p>
                    <button onClick={() => addToCart(product)}>Add to Cart</button>
                </div>
            ))}
        </div>
    );
}
```

---

## When to Use Each Approach

| Approach | Use When |
|----------|----------|
| **useState** | Simple local component state |
| **Props** | Parent-child communication (1-2 levels) |
| **Context API** | Global state, theme, auth, language |
| **useReducer** | Complex state logic with multiple actions |
| **Redux** | Large apps, complex state, time-travel debugging |

---

## Best Practices

1. ✅ **Keep state as local as possible**
2. ✅ **Use Context for global state** (user, theme)
3. ✅ **Use useReducer for complex state**
4. ✅ **Lift state up** only when needed
5. ✅ **Use Redux for large applications**
6. ❌ **Don't overuse Context** (performance issues)
7. ❌ **Don't put everything in global state**

---

## Summary

**State Management Options:**
- **useState** - Local component state
- **Context API** - Global state without prop drilling
- **useReducer** - Complex state logic
- **Redux** - Enterprise-level state management

Choose based on application complexity and requirements!
