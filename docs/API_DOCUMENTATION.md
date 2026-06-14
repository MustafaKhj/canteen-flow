# API Documentation

Base URL: http://localhost:5000

## Auth
- POST /api/auth/register
- POST /api/auth/login

## Menu
- GET /api/menu
- POST /api/menu admin only
- PUT /api/menu/:item_id admin only
- DELETE /api/menu/:item_id admin only

## Orders
- POST /api/orders student only
- GET /api/orders role-aware list
- GET /api/orders/:order_id
- PATCH /api/orders/:order_id/status staff/admin only

## Feedback
- POST /api/feedback student only
- GET /api/feedback staff/admin only

## Admin
- GET /api/admin/dashboard admin/staff
- GET /api/admin/inventory admin/staff
- POST /api/admin/inventory admin
- PATCH /api/admin/inventory/:inventory_id admin/staff
- POST /api/admin/forecast admin/staff

All protected endpoints require:
Authorization: Bearer <token>
