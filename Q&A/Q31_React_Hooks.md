# Question 31: What are React hooks? Which ones do you use most often?

## Answer

### What are React Hooks?

**Hooks** are functions that let you use React features (like state and lifecycle methods) in functional components. Introduced in React 16.8.

**Before Hooks**: Only class components could use state and lifecycle  
**After Hooks**: Functional components can do everything!

---

## 1. useState - State Management

**Most commonly used hook!**

```jsx
import { useState } from 'react';

function Counter() {
    const [count, setCount] = useState(0); // [value, setter]
    
    return (
        <div>
            <p>Count: {count}</p>
            <button onClick={() => setCount(count + 1)}>+</button>
            <button onClick={() => setCount(prev => prev - 1)}>-</button>
        </div>
    );
}

// Multiple states
function Form() {
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [age, setAge] = useState(0);
    
    // Or single object state
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        age: 0
    });
    
    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };
}
```

---

## 2. useEffect - Side Effects

**Second most commonly used!**

### Basic Usage

```jsx
import { useEffect } from 'react';

function UserProfile({ userId }) {
    const [user, setUser] = useState(null);
    
    // Runs after every render
    useEffect(() => {
        console.log('Component rendered');
    });
    
    // Runs only once (on mount)
    useEffect(() => {
        console.log('Component mounted');
    }, []); // Empty dependency array
    
    // Runs when userId changes
    useEffect(() => {
        fetchUser(userId);
    }, [userId]); // Dependency array
    
    // Cleanup function
    useEffect(() => {
        const timer = setInterval(() => {
            console.log('Tick');
        }, 1000);
        
        // Cleanup on unmount
        return () => {
            clearInterval(timer);
        };
    }, []);
    
    const fetchUser = async (id) => {
        const response = await fetch(`/api/users/${id}`);
        const data = await response.json();
        setUser(data);
    };
    
    return <div>{user?.name}</div>;
}
```

### Real-World Example: Fetch Data

```jsx
function ProductList() {
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    
    useEffect(() => {
        let isMounted = true; // Prevent state update if unmounted
        
        const fetchProducts = async () => {
            try {
                setLoading(true);
                const response = await fetch('/api/products');
                const data = await response.json();
                
                if (isMounted) {
                    setProducts(data);
                    setLoading(false);
                }
            } catch (err) {
                if (isMounted) {
                    setError(err.message);
                    setLoading(false);
                }
            }
        };
        
        fetchProducts();
        
        return () => {
            isMounted = false; // Cleanup
        };
    }, []); // Run once on mount
    
    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error}</div>;
    
    return (
        <div>
            {products.map(product => (
                <div key={product.id}>{product.name}</div>
            ))}
        </div>
    );
}
```

---

## 3. useContext - Access Context

```jsx
import { createContext, useContext } from 'react';

const ThemeContext = createContext();

function App() {
    const [theme, setTheme] = useState('light');
    
    return (
        <ThemeContext.Provider value={{ theme, setTheme }}>
            <Header />
            <Content />
        </ThemeContext.Provider>
    );
}

function Header() {
    const { theme, setTheme } = useContext(ThemeContext);
    
    return (
        <div style={{ background: theme === 'light' ? '#fff' : '#000' }}>
            <button onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}>
                Toggle Theme
            </button>
        </div>
    );
}
```

---

## 4. useRef - Reference DOM Elements

```jsx
import { useRef, useEffect } from 'react';

function TextInput() {
    const inputRef = useRef(null);
    
    useEffect(() => {
        // Focus input on mount
        inputRef.current.focus();
    }, []);
    
    const handleClick = () => {
        inputRef.current.value = '';
        inputRef.current.focus();
    };
    
    return (
        <div>
            <input ref={inputRef} type="text" />
            <button onClick={handleClick}>Clear & Focus</button>
        </div>
    );
}

// Storing mutable values (doesn't cause re-render)
function Timer() {
    const [count, setCount] = useState(0);
    const intervalRef = useRef(null);
    
    useEffect(() => {
        intervalRef.current = setInterval(() => {
            setCount(c => c + 1);
        }, 1000);
        
        return () => clearInterval(intervalRef.current);
    }, []);
    
    const stopTimer = () => {
        clearInterval(intervalRef.current);
    };
    
    return (
        <div>
            <p>Count: {count}</p>
            <button onClick={stopTimer}>Stop</button>
        </div>
    );
}
```

---

## 5. useMemo - Memoize Expensive Calculations

```jsx
import { useMemo } from 'react';

function ProductList({ products, filter }) {
    // Only recalculates when products or filter changes
    const filteredProducts = useMemo(() => {
        console.log('Filtering products...');
        return products.filter(p => 
            p.name.toLowerCase().includes(filter.toLowerCase())
        );
    }, [products, filter]);
    
    return (
        <div>
            {filteredProducts.map(product => (
                <div key={product.id}>{product.name}</div>
            ))}
        </div>
    );
}

// Without useMemo, filtering happens on every render!
```

---

## 6. useCallback - Memoize Functions

```jsx
import { useCallback } from 'react';

function Parent() {
    const [count, setCount] = useState(0);
    const [other, setOther] = useState(0);
    
    // Without useCallback: new function on every render
    // With useCallback: same function reference if dependencies don't change
    const handleClick = useCallback(() => {
        console.log('Button clicked');
        setCount(c => c + 1);
    }, []); // No dependencies - never changes
    
    return (
        <div>
            <p>Count: {count}</p>
            <Child onClick={handleClick} />
            <button onClick={() => setOther(other + 1)}>Other: {other}</button>
        </div>
    );
}

// Child won't re-render when Parent's 'other' changes
const Child = React.memo(({ onClick }) => {
    console.log('Child rendered');
    return <button onClick={onClick}>Click me</button>;
});
```

---

## 7. useReducer - Complex State Logic

```jsx
import { useReducer } from 'react';

const initialState = { count: 0 };

function reducer(state, action) {
    switch (action.type) {
        case 'increment':
            return { count: state.count + 1 };
        case 'decrement':
            return { count: state.count - 1 };
        case 'reset':
            return initialState;
        default:
            throw new Error();
    }
}

function Counter() {
    const [state, dispatch] = useReducer(reducer, initialState);
    
    return (
        <div>
            Count: {state.count}
            <button onClick={() => dispatch({ type: 'increment' })}>+</button>
            <button onClick={() => dispatch({ type: 'decrement' })}>-</button>
            <button onClick={() => dispatch({ type: 'reset' })}>Reset</button>
        </div>
    );
}
```

---

## 8. Custom Hooks - Reusable Logic

```jsx
// Custom hook for fetching data
function useFetch(url) {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    
    useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true);
                const response = await fetch(url);
                const json = await response.json();
                setData(json);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };
        
        fetchData();
    }, [url]);
    
    return { data, loading, error };
}

// Usage
function ProductList() {
    const { data: products, loading, error } = useFetch('/api/products');
    
    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error}</div>;
    
    return (
        <div>
            {products.map(p => <div key={p.id}>{p.name}</div>)}
        </div>
    );
}

// Custom hook for local storage
function useLocalStorage(key, initialValue) {
    const [value, setValue] = useState(() => {
        const stored = localStorage.getItem(key);
        return stored ? JSON.parse(stored) : initialValue;
    });
    
    useEffect(() => {
        localStorage.setItem(key, JSON.stringify(value));
    }, [key, value]);
    
    return [value, setValue];
}

// Usage
function Settings() {
    const [theme, setTheme] = useLocalStorage('theme', 'light');
    
    return (
        <button onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}>
            Current: {theme}
        </button>
    );
}
```

---

## Most Commonly Used Hooks (in order)

### 1. useState ⭐⭐⭐
**Use**: Component state
**Frequency**: Almost every component

### 2. useEffect ⭐⭐⭐
**Use**: Side effects (API calls, subscriptions)
**Frequency**: Very common

### 3. useContext ⭐⭐
**Use**: Access global state
**Frequency**: Common in larger apps

### 4. useRef ⭐⭐
**Use**: DOM references, mutable values
**Frequency**: Moderate

### 5. useMemo ⭐
**Use**: Optimize expensive calculations
**Frequency**: When performance needed

### 6. useCallback ⭐
**Use**: Optimize function references
**Frequency**: With React.memo

### 7. useReducer ⭐
**Use**: Complex state logic
**Frequency**: Alternative to useState

### 8. Custom Hooks ⭐⭐
**Use**: Reusable logic
**Frequency**: Common in clean code

---

## Rules of Hooks

1. ✅ **Only call at the top level** (not in loops, conditions, or nested functions)
2. ✅ **Only call from React functions** (components or custom hooks)
3. ✅ **Custom hooks must start with "use"**

```jsx
// ❌ BAD
function Component() {
    if (condition) {
        useState(0); // Don't call conditionally!
    }
}

// ✅ GOOD
function Component() {
    const [count, setCount] = useState(0);
    
    if (condition) {
        // Use the state here
    }
}
```

---

## Real-World Example: Complete Component

```jsx
import { useState, useEffect, useCallback, useMemo } from 'react';

function ProductDashboard() {
    const [products, setProducts] = useState([]);
    const [filter, setFilter] = useState('');
    const [loading, setLoading] = useState(true);
    
    // Fetch products
    useEffect(() => {
        fetch('/api/products')
            .then(res => res.json())
            .then(data => {
                setProducts(data);
                setLoading(false);
            });
    }, []);
    
    // Memoized filtered products
    const filteredProducts = useMemo(() => {
        return products.filter(p =>
            p.name.toLowerCase().includes(filter.toLowerCase())
        );
    }, [products, filter]);
    
    // Memoized callback
    const handleDelete = useCallback((id) => {
        setProducts(products.filter(p => p.id !== id));
    }, [products]);
    
    if (loading) return <div>Loading...</div>;
    
    return (
        <div>
            <input 
                value={filter}
                onChange={(e) => setFilter(e.target.value)}
                placeholder="Search..."
            />
            <p>Showing {filteredProducts.length} products</p>
            {filteredProducts.map(product => (
                <div key={product.id}>
                    {product.name}
                    <button onClick={() => handleDelete(product.id)}>Delete</button>
                </div>
            ))}
        </div>
    );
}
```

---

## Summary

**Essential Hooks:**
- **useState** - State in functional components
- **useEffect** - Side effects and lifecycle
- **useContext** - Access context values
- **useRef** - DOM refs and mutable values
- **useMemo** - Optimize calculations
- **useCallback** - Optimize function references
- **useReducer** - Complex state management
- **Custom Hooks** - Reusable logic

Hooks make functional components as powerful as class components!
