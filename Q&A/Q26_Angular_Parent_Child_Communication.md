# Question 26: How do you communicate from parent component to child component in Angular?

## Answer

In Angular, there are several ways to communicate between parent and child components. Let me explain each method with examples.

---

## 1. @Input() - Parent to Child (Most Common)

**Use**: Pass data from parent to child

### Parent Component

```typescript
// parent.component.ts
import { Component } from '@angular/core';

@Component({
  selector: 'app-parent',
  template: `
    <h1>Parent Component</h1>
    <app-child 
      [userName]="parentName"
      [userAge]="parentAge"
      [isActive]="isUserActive">
    </app-child>
  `
})
export class ParentComponent {
  parentName = 'John Doe';
  parentAge = 25;
  isUserActive = true;
}
```

### Child Component

```typescript
// child.component.ts
import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-child',
  template: `
    <div class="child">
      <h2>Child Component</h2>
      <p>Name: {{ userName }}</p>
      <p>Age: {{ userAge }}</p>
      <p>Status: {{ isActive ? 'Active' : 'Inactive' }}</p>
    </div>
  `
})
export class ChildComponent {
  @Input() userName: string = '';
  @Input() userAge: number = 0;
  @Input() isActive: boolean = false;
}
```

### With Alias

```typescript
export class ChildComponent {
  @Input('userName') name: string = ''; // External name: userName, Internal: name
}

// Usage in parent
<app-child [userName]="parentName"></app-child>
```

---

## 2. @Output() and EventEmitter - Child to Parent

**Use**: Send data/events from child to parent

### Child Component

```typescript
// child.component.ts
import { Component, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-child',
  template: `
    <button (click)="sendMessage()">Send to Parent</button>
    <button (click)="sendData()">Send Data</button>
  `
})
export class ChildComponent {
  @Output() messageEvent = new EventEmitter<string>();
  @Output() dataEvent = new EventEmitter<any>();
  
  sendMessage() {
    this.messageEvent.emit('Hello from Child!');
  }
  
  sendData() {
    const data = {
      id: 1,
      name: 'Product',
      price: 99.99
    };
    this.dataEvent.emit(data);
  }
}
```

### Parent Component

```typescript
// parent.component.ts
@Component({
  selector: 'app-parent',
  template: `
    <app-child 
      (messageEvent)="receiveMessage($event)"
      (dataEvent)="receiveData($event)">
    </app-child>
    <p>Message from child: {{ childMessage }}</p>
  `
})
export class ParentComponent {
  childMessage: string = '';
  
  receiveMessage(message: string) {
    this.childMessage = message;
    console.log('Received:', message);
  }
  
  receiveData(data: any) {
    console.log('Received data:', data);
  }
}
```

---

## 3. Two-Way Binding with [(ngModel)]

```typescript
// child.component.ts
import { Component, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-child',
  template: `
    <input 
      [value]="userName" 
      (input)="onUserNameChange($event)">
  `
})
export class ChildComponent {
  @Input() userName: string = '';
  @Output() userNameChange = new EventEmitter<string>();
  
  onUserNameChange(event: any) {
    this.userNameChange.emit(event.target.value);
  }
}

// parent.component.ts
@Component({
  selector: 'app-parent',
  template: `
    <app-child [(userName)]="parentName"></app-child>
    <p>Name: {{ parentName }}</p>
  `
})
export class ParentComponent {
  parentName = 'John';
}
```

---

## 4. @ViewChild - Parent Access Child's Methods/Properties

```typescript
// child.component.ts
@Component({
  selector: 'app-child',
  template: `<p>Count: {{ count }}</p>`
})
export class ChildComponent {
  count = 0;
  
  increment() {
    this.count++;
  }
  
  reset() {
    this.count = 0;
  }
  
  getMessage(): string {
    return 'Message from child';
  }
}

// parent.component.ts
import { Component, ViewChild, AfterViewInit } from '@angular/core';

@Component({
  selector: 'app-parent',
  template: `
    <app-child #childComponent></app-child>
    <button (click)="callChildMethod()">Call Child Method</button>
    <button (click)="accessChildProperty()">Access Child Property</button>
  `
})
export class ParentComponent implements AfterViewInit {
  @ViewChild('childComponent') child!: ChildComponent;
  
  ngAfterViewInit() {
    // Can access child after view init
    console.log(this.child.count);
  }
  
  callChildMethod() {
    this.child.increment();
    const message = this.child.getMessage();
    console.log(message);
  }
  
  accessChildProperty() {
    console.log('Child count:', this.child.count);
  }
}
```

---

## 5. Service (Shared Data) - Any to Any

```typescript
// shared.service.ts
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SharedService {
  private messageSource = new BehaviorSubject<string>('default message');
  currentMessage = this.messageSource.asObservable();
  
  private dataSource = new BehaviorSubject<any>(null);
  currentData = this.dataSource.asObservable();
  
  changeMessage(message: string) {
    this.messageSource.next(message);
  }
  
  updateData(data: any) {
    this.dataSource.next(data);
  }
}

// parent.component.ts
@Component({
  selector: 'app-parent',
  template: `
    <input [(ngModel)]="message">
    <button (click)="sendMessage()">Send via Service</button>
    <app-child></app-child>
  `
})
export class ParentComponent {
  message: string = '';
  
  constructor(private sharedService: SharedService) {}
  
  sendMessage() {
    this.sharedService.changeMessage(this.message);
  }
}

// child.component.ts
@Component({
  selector: 'app-child',
  template: `
    <p>Received: {{ message }}</p>
  `
})
export class ChildComponent implements OnInit {
  message: string = '';
  
  constructor(private sharedService: SharedService) {}
  
  ngOnInit() {
    this.sharedService.currentMessage.subscribe(
      message => this.message = message
    );
  }
}
```

---

## Real-World Example: Product List and Details

```typescript
// product.model.ts
export interface Product {
  id: number;
  name: string;
  price: number;
  category: string;
}

// product-list.component.ts (Parent)
@Component({
  selector: 'app-product-list',
  template: `
    <h1>Products</h1>
    <app-product-item
      *ngFor="let product of products"
      [product]="product"
      (productSelected)="onProductSelected($event)"
      (deleteProduct)="onDeleteProduct($event)">
    </app-product-item>
    
    <app-product-details
      [selectedProduct]="selected"
      (closeDetails)="selected = null">
    </app-product-details>
  `
})
export class ProductListComponent {
  products: Product[] = [
    { id: 1, name: 'Laptop', price: 999, category: 'Electronics' },
    { id: 2, name: 'Phone', price: 699, category: 'Electronics' },
    { id: 3, name: 'Desk', price: 299, category: 'Furniture' }
  ];
  
  selected: Product | null = null;
  
  onProductSelected(product: Product) {
    this.selected = product;
  }
  
  onDeleteProduct(productId: number) {
    this.products = this.products.filter(p => p.id !== productId);
    if (this.selected?.id === productId) {
      this.selected = null;
    }
  }
}

// product-item.component.ts (Child)
@Component({
  selector: 'app-product-item',
  template: `
    <div class="product-card" (click)="selectProduct()">
      <h3>{{ product.name }}</h3>
      <p>Price: ${{ product.price }}</p>
      <p>Category: {{ product.category }}</p>
      <button (click)="deleteClick($event)">Delete</button>
    </div>
  `,
  styles: [`
    .product-card {
      border: 1px solid #ccc;
      padding: 15px;
      margin: 10px;
      cursor: pointer;
    }
  `]
})
export class ProductItemComponent {
  @Input() product!: Product;
  @Output() productSelected = new EventEmitter<Product>();
  @Output() deleteProduct = new EventEmitter<number>();
  
  selectProduct() {
    this.productSelected.emit(this.product);
  }
  
  deleteClick(event: Event) {
    event.stopPropagation(); // Prevent card click
    this.deleteProduct.emit(this.product.id);
  }
}

// product-details.component.ts (Child)
@Component({
  selector: 'app-product-details',
  template: `
    <div *ngIf="selectedProduct" class="details-panel">
      <button (click)="close()">Close</button>
      <h2>{{ selectedProduct.name }}</h2>
      <p><strong>Price:</strong> ${{ selectedProduct.price }}</p>
      <p><strong>Category:</strong> {{ selectedProduct.category }}</p>
      <p><strong>ID:</strong> {{ selectedProduct.id }}</p>
    </div>
  `
})
export class ProductDetailsComponent {
  @Input() selectedProduct: Product | null = null;
  @Output() closeDetails = new EventEmitter<void>();
  
  close() {
    this.closeDetails.emit();
  }
}
```

---

## Summary Table

| Method | Direction | Use Case |
|--------|-----------|----------|
| **@Input()** | Parent → Child | Pass data down |
| **@Output()** | Child → Parent | Send events/data up |
| **@ViewChild** | Parent → Child | Access child methods/properties |
| **Service** | Any ↔ Any | Share data across components |
| **Two-way binding** | Parent ↔ Child | Sync data both ways |

---

## Best Practices

1. ✅ **Use @Input() for parent-to-child data flow**
2. ✅ **Use @Output() for child-to-parent events**
3. ✅ **Use Services for unrelated components**
4. ✅ **Keep components loosely coupled**
5. ✅ **Unsubscribe from observables** in ngOnDestroy
6. ❌ **Don't overuse @ViewChild** (tight coupling)
7. ❌ **Don't use services for simple parent-child** communication

---

## Component Communication Lifecycle

```typescript
// Complete example with lifecycle hooks
@Component({
  selector: 'app-child',
  template: `<p>{{ data }}</p>`
})
export class ChildComponent implements OnInit, OnChanges, OnDestroy {
  @Input() data: string = '';
  @Output() dataChange = new EventEmitter<string>();
  
  ngOnInit() {
    console.log('Child initialized with data:', this.data);
  }
  
  ngOnChanges(changes: SimpleChanges) {
    if (changes['data']) {
      console.log('Data changed from', 
        changes['data'].previousValue, 
        'to', 
        changes['data'].currentValue);
    }
  }
  
  ngOnDestroy() {
    console.log('Child destroyed');
  }
  
  updateData(newData: string) {
    this.data = newData;
    this.dataChange.emit(newData);
  }
}
```

---

## Quick Reference

```typescript
// Parent → Child
<app-child [data]="parentData"></app-child>

// Child → Parent
<app-child (event)="handleEvent($event)"></app-child>

// Two-way
<app-child [(data)]="parentData"></app-child>

// ViewChild
@ViewChild(ChildComponent) child!: ChildComponent;

// Service
constructor(private service: SharedService) {}
```

Master these patterns for effective Angular component communication!
