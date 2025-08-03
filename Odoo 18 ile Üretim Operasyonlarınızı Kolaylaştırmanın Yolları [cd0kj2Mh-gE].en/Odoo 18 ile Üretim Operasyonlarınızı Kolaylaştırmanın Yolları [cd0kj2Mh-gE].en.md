The following content is extracted and cleaned from the provided subtitle file, `Odoo 18 ile Üretim Operasyonlarınızı Kolaylaştırmanın Yolları [cd0kj2Mh-gE].en.vtt`.

---

## **Odoo 18: Streamlining Production Operations Tutorial**

This tutorial outlines how Odoo 18 can help simplify and integrate your production operations, from sales to purchasing, inventory, production tracking, and quality control.

### **Introduction**

The presentation begins with an introduction to Odoo 18 and its capabilities in streamlining production processes. Disconnected operations in businesses, often relying on manual tools like Excel, emails, or notebooks, lead to significant financial losses and inefficiencies.

*   **Problem Highlighted:** 36% of companies lose millions annually due to non-integrated systems; a medium-sized company faces an average annual inefficiency cost of $400,000. Issues include poor coordination between departments (sales, purchasing, production, warehouse), inability to plan production, incorrect customer deadlines, raw material procurement uncertainties, lack of inventory tracking, unclear production costs, inefficient workforce/equipment planning, and difficulty managing Bills of Materials (BOMs) and revisions.
*   **Odoo's Integrated Solution:** Odoo offers an Enterprise Resource Planning (ERP) system with approximately 82 integrated modules. This integration significantly improves efficiency:
    *   23% faster growth for companies using integrated systems.
    *   47% reduction in order processing time.
    *   35% reduction in production delays.
    *   All business operations (sales, production, purchasing, inventory, accounting, CRM, project tracking, email marketing, etc.) are managed from a single platform.

### **Getting Started with Odoo 18**

1.  **Explore Odoo Modules:**
    *   Navigate to the "Applications" tab.
    *   You can try any of the 82+ modules for free for 14 days without limitations (add unlimited users).
    *   After 14 days, if no purchase is made, your demo database will be automatically deleted.

2.  **Schedule a Personalized Demo:**
    *   Scan the provided QR code or visit odoo.com.
    *   Schedule an introductory meeting (approx. 30-60 minutes) with an Odoo business consultant.
    *   In this meeting, discuss your specific demands, current workflow, and how Odoo can address your needs.
    *   A tailored demo presentation will be prepared for you based on your industry and requirements (e.g., a furniture company flow). There is no fee for these demo meetings.

### **Odoo 18 Production Tutorial Steps (Furniture Company Example)**

This section details the practical steps within Odoo for managing production, using a furniture company producing "Wenge Tables" as an example.

#### **Step 1: Configure Workstations (Production Module)**

1.  **Define Work Centers:**
    *   Go to the "Production" module.
    *   Set up your production workstations (e.g., Sizing 1, Sizing 2, Edge Banding, Hole Punching, Assembly, Packaging).
    *   Configure settings for each work center:
        *   **Time Efficiency:** How efficiently work is done.
        *   **Performance Target:** Expected output.
        *   **Setup Time & Cleaning Time:** Time needed before/after operations.
        *   **Assigned Employees:** Specify which employees can work at this station.
        *   **Cost per Hour:** Define the hourly cost (e.g., 150 TL per hour) for accurate production cost calculation. This can include electricity, rent, and employee salaries.
        *   **Alternative Work Centers:** Designate alternative machines/workstations (e.g., Sizing 2 is an alternative to Sizing 1). If one is busy, Odoo automatically routes production orders to the available alternative.
        *   **Tags:** Add tags for categorization (e.g., "Brand 1" for machine brands).

#### **Step 2: Manage Products & Categories (Inventory Module)**

1.  **Product Overview:**
    *   Access "Products" from the "Inventory" module (or Sales/Purchase modules).
    *   View products with "Goods" status (vs. "Service" or "Combo").
    *   Categorize products: "Raw Material", "Semi-Finished Product", "Finished Product".
    *   Use different view types (Kanban, List, Catalog) for better visualization.
2.  **Product Details & Costing:**
    *   **Reference Codes:** Assign unique alphanumeric codes to products.
    *   **Sales Prices:** Set sales prices for finished products (raw/semi-finished products typically have no sales price).
    *   **Cost Calculation:** Odoo automatically calculates product costs based on raw material costs and operation costs from recipes (e.g., a Wenge Table Top cost of 429.60 is calculated, not manually entered).
    *   **Cost Methods:**
        *   **Standard Cost:** Manually entered cost (requires manual updates).
        *   **First-In-First-Out (FIFO):** Uses the cost of the oldest inventory first.
        *   **Average Cost:** Calculates cost based on the average purchase price (commonly used in Turkey).
    *   **Stock & Forecast:** View current stock levels and forecasted stock based on incoming/outgoing orders.
    *   **Traceability (Lot/Serial Numbers):** Enable tracking by lot/serial numbers for complete retroactive flow visibility. This allows you to track:
        *   Which raw materials were used.
        *   What operations were performed.
        *   Quality control results (including photos).
        *   Which customer received the specific lot.
3.  **Replenishment Rules:**
    *   Set **Minimum/Maximum Stock Rules** (e.g., if Wenge Table Top stock drops below 30 units, trigger production for 50 units). This automatically generates production or purchase orders.
    *   Implement **Make-to-Order (MTO)** for finished products (e.g., "Fulfillment on Order" for Wenge Table), where a production order is automatically created only when a sales order is received.
    *   Use **Putaway Rules** for automatic internal transfers within the warehouse (e.g., from raw material warehouse to semi-finished goods warehouse).
4.  **Quality Control Points:**
    *   Define **Quality Control Points** for specific products, quantities, or operations.
    *   Assign a responsible person.
    *   Set **Frequency of Checks** (e.g., every 5th product, or every operation).
    *   Choose **Control Type:**
        *   **Instructions:** Provide guidelines (e.g., check according to drawing). You can upload technical drawings.
        *   **Take a Picture:** Require photo upload (e.g., for visual quality check). The QC cannot be completed without a photo.
        *   **Pass/Fail:** Simple pass or fail check.
        *   **Measure:** Enter a measurement and define acceptable tolerances. If the measurement is outside tolerance, it automatically fails.

#### **Step 3: Define Product Recipes (Bills of Materials - BOMs)**

1.  **Create BOMs:**
    *   For a semi-finished product (e.g., Wenge Table Top): Define inputs (e.g., 1 m² of MDF laminate, 4.20 m of PVC edge band) and operations (Sizing, Edge Banding).
    *   For a finished product (e.g., Wenge Table): Define inputs (e.g., Wenge Table Top, metal legs, screws, packaging) and operations (Hole Drilling, Assembly, Packaging).
    *   **Operations in BOM:** Specify which work center performs each operation and its estimated duration.
    *   **Readiness for Production:** Choose when production can start:
        *   "All components are available" (default, ensures all raw materials are in stock).
        *   "Components for the first operation are available" (allows production to start if only initial materials are ready).
    *   **Flexible Consumption:** Allow or block consumption of raw materials beyond the recipe, with a warning. This helps control material waste and prevents unauthorized usage.
    *   **By-Products:** Define any additional products or scraps generated during production (e.g., sawdust). These can be tracked and potentially sold.

#### **Step 4: Sales Order Management (Sales Module)**

1.  **Create a New Sales Offer:**
    *   Select a customer (e.g., "Test Customer 1").
    *   Assign a specific **Price List** to the customer, which automatically applies pricing rules (e.g., "TL Wholesale Sales Price List" for a 10% discount on orders of 10+ pieces).
    *   Set **Payment Terms** and assign a **Salesperson**.
    *   Add products to the sales order (e.g., 25 Wenge Tables). Odoo automatically applies the correct price based on the selected price list and quantity.
    *   View **Margin** (internal only, not visible to customer).
    *   Add internal **Notes** (e.g., "Special customer request").
    *   Optionally convert currency (e.g., to USD). Odoo records it in TL based on the daily Central Bank exchange rate.
2.  **Send the Offer:**
    *   Click "Send" to generate a PDF quote.
    *   Email the quote directly from Odoo. The email is integrated and tracked in the "chatter block" on the sales order.
    *   Track email replies and all communication history on the sales order.
    *   Set up **Follow-up Activities** (e.g., a reminder to "ask about offer tomorrow").
3.  **Confirm the Sales Order:**
    *   Once the customer approves, click "Confirm" to convert the offer into a sales order.
    *   This action automatically triggers related operations like production orders and delivery orders.
    *   Odoo indicates if products are not in stock (red button).

#### **Step 5: Purchasing Raw Materials (Purchasing Module)**

1.  **Review Purchase Requests:**
    *   Access the "Purchasing" module.
    *   View automatically generated "Requests for Quote (RFQ)" (marked in blue if not yet approved). These are triggered by production needs (e.g., lack of metal legs or packaging).
2.  **Manage RFQs:**
    *   Open an RFQ.
    *   Review product quantities and request prices from suppliers.
    *   Send the RFQ to the supplier via integrated email.
    *   Track email communication in the "chatter block".
    *   **Price Comparison:** Use the "Price Comparison" feature to view past offers from different suppliers for the same products, aiding negotiation.
    *   **Create Alternatives:** Request alternative offers from different suppliers and compare them side-by-side.
    *   **Confirm Order:** Once a supplier's offer is accepted, confirm the purchase order. Odoo automatically cancels other alternative offers for the same products.
3.  **Receive Products:**
    *   Go to the "Inventory" module -> "Operations" -> "Receipts".
    *   Verify the received quantities against the purchase order.
    *   Click "Validate" to automatically add the products to your stock.

#### **Step 6: Production Execution (Production Screens for Workers)**

1.  **Production Orders:**
    *   Return to the "Production" module -> "Production Orders".
    *   View automatically generated production orders (triggered by sales orders or min/max stock rules) or create new ones manually.
    *   Each production order has linked sales and purchase orders for full traceability.
    *   Assign lot/serial numbers to the finished products being produced.
2.  **Work Center Planning:**
    *   Go to "Planning" -> "Work Centers".
    *   Visualize the workload and occupancy of each workstation (e.g., Sizing 1, Sizing 2, Assembly).
    *   Colors indicate different production orders.
    *   Drag and drop production tasks to reallocate them between alternative work centers or adjust schedules.
    *   Manually adjust estimated times for operations if needed.
3.  **Blue Collar Worker Interface (Production Screen):**
    *   This simplified screen, typically displayed on tablets at work centers, is for production floor workers.
    *   Workers see their assigned production tasks.
    *   **Start/Stop Tracking:** Workers can start and stop timers for each operation, accurately tracking time spent. This data is crucial for cost calculation and productivity analysis.
    *   **Quality Control Prompts:** Odoo will prompt workers to perform required quality checks based on the defined QC points (e.g., verify drawing, take photo, enter measurements). Production cannot be completed without passing QC.
    *   **By-Product Recording:** If by-products are generated, workers can easily record quantities before completing the production.
4.  **Complete Production:**
    *   After all operations are completed and quality checks are passed, mark the production order as "Done".
    *   Odoo automatically deducts consumed raw materials from stock and adds finished products to stock.

#### **Step 7: Delivery & Invoicing (Sales & Accounting Modules)**

1.  **Deliver Products (Inventory Module):**
    *   Go to "Inventory" module -> "Operations" -> "Delivery Orders".
    *   The warehouseman can see pending deliveries (e.g., 25 Wenge Tables for "Test Customer 1").
    *   Verify the quantities and click "Validate" to ship the products. This automatically removes them from stock.
2.  **Create Invoice (Sales/Accounting Module):**
    *   From the sales order, click "Create Invoice".
    *   Choose invoicing options (e.g., prepayment, full invoice).
    *   Approve the invoice. This updates your accounting records.
    *   Send the invoice to the customer via integrated email.
    *   **Turkish Digital Solutions:** Odoo can integrate with e-invoice, e-delivery note, and e-call systems for compliance in Turkey.

#### **Step 8: Reporting & Analytics**

1.  **Stock Reporting:**
    *   View real-time stock levels of all products (raw, semi-finished, finished).
    *   Track forecasted stock based on production and sales orders.
2.  **Production Analysis:**
    *   Generate reports on production costs, quantities produced over specific periods, and productivity per work center.
    *   Compare actual time spent vs. estimated time for operations, identifying areas for improvement (red for over-budget, green for under-budget).
3.  **Traceability Report:**
    *   Access detailed retrospective tracking for any product using its lot/serial number.
    *   See the entire journey: from which sales order it originated, through which production orders, what raw materials were used (and from which purchase orders), who performed which quality controls, and when it was delivered to the customer.
4.  **Purchasing Reports:**
    *   Analyze purchase history by supplier, product, quantity, and total cost.
    *   Access historical quote comparisons.

### **Odoo Project Implementation & Support**

*   **Dedicated Team:** Odoo provides a dedicated project manager and technical consultants (often Turkish-speaking and experienced in your industry).
*   **Project Phases:**
    1.  **Weekly Meetings:** Regular meetings to discuss progress and gather requirements.
    2.  **Configuration:** System setup tailored to your workflow.
    3.  **Data Import:** Embedding your products, contacts, and suppliers into the system.
    4.  **Training:** Comprehensive training for your employees on using Odoo.
    5.  **Testing Environment:** A sandbox environment where you can practice and make mistakes before going live with real data.
    6.  **Go-Live:** Transition to the live system.
    7.  **Account Management:** Post-go-live, a dedicated account manager provides ongoing support and helps with future projects (e.g., e-commerce, website).
*   **Customization:**
    *   **Frontend UI:** Minor UI adjustments (adding/removing fields) can be done easily using the "Studio" application without coding.
    *   **Backend Development:** For complex customizations requiring code changes, a "special plan" with Odoo's development team is needed (incurs extra effort/cost). Odoo aims to keep solutions as standard as possible for long-term maintainability.

---