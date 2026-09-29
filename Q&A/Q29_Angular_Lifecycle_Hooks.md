# Question 29: Explain the Angular lifecycle hooks. Which ones have you used most frequently?

## Answer

### What are Lifecycle Hooks?

**Lifecycle hooks** are methods that Angular calls at specific moments in a component's lifecycle, from creation to destruction. They let you tap into key moments and perform custom logic.

---

## Angular Component Lifecycle (in order)

```
1. constructor()          // Class instantiation
    ↓
2. ngOnChanges()         // When @Input() values change
    ↓
3. ngOnInit()            // After first ngOnChanges
    ↓
4. ngDoCheck()           // Every change detection cycle
    ↓
5. ngAfterContentInit()  // After content projection
    ↓
6. ngAfterContentChecked() // After every content check
    ↓
7. ngAfterViewInit()     // After view initialization
    ↓
8. ngAfterViewChecked()  // After every view check
    ↓
9. ngOnDestroy()         // Before component destruction
```

---

## Most Commonly Used Hooks ⭐

### 1. ngOnInit() - Most Used! ⭐⭐⭐

**When**: Called once after the first `ngOnChanges()`, after component is initialized  
**Use for**: Initialization logic, API calls, setup

```typescript
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-product-list',
  template: `
    <div *ngIf="loading">Loading...</div>
    <div *ngFor="let product of products">
      {{ product.name }}
    </div>
  `
})
export class ProductListComponent implements OnInit {
  products: Product[] = [];
  loading = false;
  
  constructor(private productService: ProductService) {
    // DON'T make API calls here!
    console.log('Constructor called');
  }
  
  ngOnInit(): void {
    // ✅ GOOD - Make API calls here
    console.log('ngOnInit called');
    this.loadProducts();
  }
  
  private loadProducts(): void {
    this.loading = true;
    this.productService.getProducts().subscribe({
      next: (data) => {
        this.products = data;
        this.loading = false;
      },
      error: (error) => {
        console.error('Error loading products', error);
        this.loading = false;
      }
    });
  }
}
```

**Why ngOnInit instead of constructor?**
- Component inputs are available
- Dependency injection is complete
- Best practice for initialization
- Easier to test

---

### 2. ngOnChanges() - Very Common ⭐⭐⭐

**When**: Called whenever `@Input()` property values change  
**Use for**: React to input changes, validation

```typescript
import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';

@Component({
  selector: 'app-user-profile',
  template: `
    <div>
      <h2>{{ user?.name }}</h2>
      <p>Age: {{ calculatedAge }}</p>
    </div>
  `
})
export class UserProfileComponent implements OnChanges {
  @Input() user: User;
  @Input() birthDate: Date;
  
  calculatedAge: number;
  
  ngOnChanges(changes: SimpleChanges): void {
    console.log('ngOnChanges called', changes);
    
    // Check if specific input changed
    if (changes['birthDate']) {
      console.log('Birth date changed');
      console.log('Previous:', changes['birthDate'].previousValue);
      console.log('Current:', changes['birthDate'].currentValue);
      console.log('First change?', changes['birthDate'].firstChange);
      
      this.calculateAge();
    }
    
    if (changes['user']) {
      console.log('User changed');
      this.updateUserProfile();
    }
  }
  
  private calculateAge(): void {
    if (this.birthDate) {
      const today = new Date();
      const birth = new Date(this.birthDate);
      this.calculatedAge = today.getFullYear() - birth.getFullYear();
    }
  }
  
  private updateUserProfile(): void {
    // Perform actions when user changes
  }
}
```

---

### 3. ngOnDestroy() - Important for Cleanup ⭐⭐⭐

**When**: Called just before component is destroyed  
**Use for**: Cleanup - unsubscribe, clear timers, detach event handlers

```typescript
import { Component, OnInit, OnDestroy } from '@angular/core';
import { Subscription, interval } from 'rxjs';

@Component({
  selector: 'app-timer',
  template: `<p>Timer: {{ counter }}</p>`
})
export class TimerComponent implements OnInit, OnDestroy {
  counter = 0;
  private timerSubscription: Subscription;
  private intervalId: any;
  
  ngOnInit(): void {
    // Start a timer
    this.timerSubscription = interval(1000).subscribe(() => {
      this.counter++;
    });
    
    // Set interval
    this.intervalId = setInterval(() => {
      console.log('Tick');
    }, 1000);
  }
  
  ngOnDestroy(): void {
    console.log('Component being destroyed');
    
    // ✅ IMPORTANT - Prevent memory leaks
    if (this.timerSubscription) {
      this.timerSubscription.unsubscribe();
    }
    
    if (this.intervalId) {
      clearInterval(this.intervalId);
    }
  }
}

// Better pattern with takeUntil
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';

@Component({
  selector: 'app-better-timer',
  template: `<p>Timer: {{ counter }}</p>`
})
export class BetterTimerComponent implements OnInit, OnDestroy {
  counter = 0;
  private destroy$ = new Subject<void>();
  
  constructor(private dataService: DataService) {}
  
  ngOnInit(): void {
    // All subscriptions automatically unsubscribe
    interval(1000)
      .pipe(takeUntil(this.destroy$))
      .subscribe(() => this.counter++);
    
    this.dataService.getData()
      .pipe(takeUntil(this.destroy$))
      .subscribe(data => console.log(data));
  }
  
  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }
}
```

---

### 4. ngAfterViewInit() - Common for DOM Access ⭐⭐

**When**: Called after component's view (and child views) are initialized  
**Use for**: Access DOM elements, child components via @ViewChild

```typescript
import { Component, AfterViewInit, ViewChild, ElementRef } from '@angular/core';

@Component({
  selector: 'app-search',
  template: `
    <input #searchInput type="text" placeholder="Search...">
    <app-child-component #childComponent></app-child-component>
  `
})
export class SearchComponent implements AfterViewInit {
  @ViewChild('searchInput') searchInput: ElementRef;
  @ViewChild('childComponent') childComponent: ChildComponent;
  
  ngAfterViewInit(): void {
    // ✅ NOW we can access DOM elements
    console.log('View initialized');
    
    // Focus input
    this.searchInput.nativeElement.focus();
    
    // Access child component
    console.log('Child data:', this.childComponent.someData);
    this.childComponent.someMethod();
  }
}
```

---

## Less Commonly Used Hooks

### 5. ngDoCheck()

**When**: During every change detection cycle  
**Use for**: Custom change detection (use sparingly - performance impact!)

```typescript
import { Component, DoCheck, Input } from '@angular/core';

@Component({
  selector: 'app-custom-check',
  template: `<p>{{ data.value }}</p>`
})
export class CustomCheckComponent implements DoCheck {
  @Input() data: any;
  private oldValue: any;
  
  ngDoCheck(): void {
    // ⚠️ Called VERY frequently - be careful!
    if (this.data.value !== this.oldValue) {
      console.log('Custom change detected');
      this.oldValue = this.data.value;
    }
  }
}
```

### 6. ngAfterContentInit()

**When**: After content projection into component  
**Use for**: Access projected content

```typescript
import { Component, AfterContentInit, ContentChild } from '@angular/core';

@Component({
  selector: 'app-container',
  template: `
    <div class="container">
      <ng-content></ng-content>
    </div>
  `
})
export class ContainerComponent implements AfterContentInit {
  @ContentChild('projectedContent') content: ElementRef;
  
  ngAfterContentInit(): void {
    console.log('Content projected:', this.content);
  }
}

// Usage:
// <app-container>
//   <div #projectedContent>This is projected content</div>
// </app-container>
```

---

## Real-World Example: Product Details Page

```typescript
import { Component, OnInit, OnDestroy, Input, OnChanges, SimpleChanges } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';

@Component({
  selector: 'app-product-details',
  template: `
    <div *ngIf="loading">Loading...</div>
    <div *ngIf="product && !loading">
      <h1>{{ product.name }}</h1>
      <p>Price: {{ product.price | currency }}</p>
      <p>{{ product.description }}</p>
    </div>
  `
})
export class ProductDetailsComponent implements OnInit, OnChanges, OnDestroy {
  @Input() productId: number;
  
  product: Product;
  loading = false;
  private destroy$ = new Subject<void>();
  
  constructor(
    private route: ActivatedRoute,
    private productService: ProductService
  ) {
    console.log('1. Constructor called');
  }
  
  ngOnChanges(changes: SimpleChanges): void {
    console.log('2. ngOnChanges called', changes);
    
    if (changes['productId'] && !changes['productId'].firstChange) {
      // Product ID changed - reload product
      this.loadProduct(this.productId);
    }
  }
  
  ngOnInit(): void {
    console.log('3. ngOnInit called');
    
    // Get product ID from route if not provided as input
    if (!this.productId) {
      this.route.params
        .pipe(takeUntil(this.destroy$))
        .subscribe(params => {
          this.productId = +params['id'];
          this.loadProduct(this.productId);
        });
    } else {
      this.loadProduct(this.productId);
    }
  }
  
  ngOnDestroy(): void {
    console.log('4. ngOnDestroy called - Cleaning up');
    this.destroy$.next();
    this.destroy$.complete();
  }
  
  private loadProduct(id: number): void {
    this.loading = true;
    
    this.productService.getProduct(id)
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (product) => {
          this.product = product;
          this.loading = false;
        },
        error: (error) => {
          console.error('Error loading product', error);
          this.loading = false;
        }
      });
  }
}
```

---

## Most Frequently Used (Priority Order)

### 1. ngOnInit() ⭐⭐⭐
- **Frequency**: Almost every component
- **Use**: Initialization, API calls, setup

### 2. ngOnDestroy() ⭐⭐⭐
- **Frequency**: When using subscriptions/timers
- **Use**: Cleanup, unsubscribe

### 3. ngOnChanges() ⭐⭐
- **Frequency**: Components with @Input()
- **Use**: React to input changes

### 4. ngAfterViewInit() ⭐⭐
- **Frequency**: When accessing DOM/child components
- **Use**: DOM manipulation, ViewChild access

### 5. Others ⭐
- **ngDoCheck**: Rarely (performance concerns)
- **ngAfterContentInit**: Rarely (content projection)
- **ngAfterViewChecked**: Very rarely (performance concerns)
- **ngAfterContentChecked**: Very rarely (performance concerns)

---

## Best Practices

1. ✅ **Always implement the interface** (e.g., `implements OnInit`)
2. ✅ **Use ngOnInit for initialization**, not constructor
3. ✅ **Always unsubscribe in ngOnDestroy** to prevent memory leaks
4. ✅ **Use takeUntil pattern** for managing subscriptions
5. ✅ **Access ViewChild in ngAfterViewInit**, not earlier
6. ❌ **Avoid heavy logic in ngDoCheck** (performance impact)
7. ❌ **Don't make HTTP calls in constructor**

---

## Common Mistakes

```typescript
// ❌ BAD - API call in constructor
constructor(private service: DataService) {
  this.service.getData().subscribe(); // Don't do this!
}

// ✅ GOOD - API call in ngOnInit
ngOnInit(): void {
  this.service.getData().subscribe();
}

// ❌ BAD - Forgot to unsubscribe
ngOnInit(): void {
  this.service.getData().subscribe(); // Memory leak!
}

// ✅ GOOD - Unsubscribe on destroy
private destroy$ = new Subject<void>();

ngOnInit(): void {
  this.service.getData()
    .pipe(takeUntil(this.destroy$))
    .subscribe();
}

ngOnDestroy(): void {
  this.destroy$.next();
  this.destroy$.complete();
}
```

---

## Summary

**Lifecycle Hook Order:**
1. constructor → ngOnChanges → ngOnInit → ... → ngOnDestroy

**Most Important:**
- **ngOnInit**: Initialization
- **ngOnDestroy**: Cleanup
- **ngOnChanges**: Input changes

**Remember:** Always clean up subscriptions and timers in ngOnDestroy!
