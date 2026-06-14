# Canteen-Flow MongoDB Database Schema

This version follows the attached project report concept but uses MongoDB for the entire database. MySQL has been removed completely.

## Collections

### users
Stores students, staff, and admins.
- _id ObjectId
- name string
- email string unique
- password_hash string
- role enum: student, staff, admin
- wallet_balance number
- created_at datetime

### menu_items
Stores the dynamic daily menu.
- _id ObjectId
- name string
- category string
- price number
- description string
- calories number
- is_special boolean
- is_available boolean
- created_at datetime
- updated_at datetime

### orders
Stores order headers.
- _id ObjectId
- user_id ObjectId ref users
- student_name string denormalized display field
- status enum: pending, in_preparation, ready, delivered, cancelled
- total_amount number
- created_at datetime
- updated_at datetime

### order_items
Stores normalized order line items separately from orders.
- _id ObjectId
- order_id ObjectId ref orders
- menu_item_id ObjectId ref menu_items
- item_name string snapshot
- category string snapshot
- quantity number
- unit_price number
- line_total number
- created_at datetime

### payments
Stores payment records.
- _id ObjectId
- order_id ObjectId unique ref orders
- user_id ObjectId ref users
- amount number
- method string
- status string
- created_at datetime

### transactions
Stores audit log for billing and order payment actions.
- _id ObjectId
- order_id ObjectId ref orders
- user_id ObjectId ref users
- type string
- amount number
- description string
- created_at datetime

### inventory
Stores ingredient and stock quantities.
- _id ObjectId
- item_name string unique
- quantity number
- unit string
- reorder_level number
- created_at datetime
- updated_at datetime

### stock_logs
Stores every inventory adjustment.
- _id ObjectId
- inventory_id ObjectId ref inventory
- change number
- reason string
- created_at datetime

### feedback
Stores student feedback on menu items.
- _id ObjectId
- order_id ObjectId ref orders
- user_id ObjectId ref users
- student_name string
- menu_item_id ObjectId ref menu_items
- menu_item_name string
- rating number 1-5
- comment string
- created_at datetime

### forecasts
Stores generated demand forecast results.
- _id ObjectId
- created_at datetime
- days_used number
- predictions array

## Normalization Approach
Even though this is MongoDB, the database is structured in a normalized/reference-based way for academic ADBMS requirements. Orders and order_items are separate collections, payments and transactions are separate collections, and inventory changes are separated into stock_logs. This avoids repeating complete order and payment data in multiple places while still using MongoDB only.
