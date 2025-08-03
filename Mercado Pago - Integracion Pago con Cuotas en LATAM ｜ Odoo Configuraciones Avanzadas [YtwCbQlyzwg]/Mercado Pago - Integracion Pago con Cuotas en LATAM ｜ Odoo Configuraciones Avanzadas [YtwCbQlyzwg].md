The content of the uploaded file `Mercado Pago - Integracion Pago con Cuotas en LATAM ｜ Odoo Configuraciones Avanzadas [YtwCbQlyzwg].vtt` has been extracted, cleaned, and structured below, followed by Odoo 18 tutorial steps.

---

## Cleaned Content from `Mercado Pago - Integracion Pago con Cuotas en LATAM ｜ Odoo Configuraciones Avanzadas [YtwCbQlyzwg].vtt`

### Introduction
Welcome to this video about Mercado Pago's new feature: integration with installment payments. My name is Daniela Cáñez, a Business Systems Analyst and localization expert. In today's video, we'll cover context, flows, configurations, a demo, and finally, a list of available resources.

### Context of Mercado Pago Integration with Odoo
*   **Mercado Pago Checkout Pro:** Odoo is integrated with Mercado Pago Checkout Pro, allowing buyers to navigate to a secure Mercado Pago page to complete their transaction safely.
*   **New Installment Payment Option:** Starting with Odoo version 18.4, the installment payment option will be available. This provides customers greater flexibility and helps increase sales.
*   **Available Countries for Mercado Pago:** Mexico, Argentina, Uruguay, Peru, Colombia, Chile, and Brazil.
*   **Supported Operations:** Electronic commerce (e-commerce) and online payment for sales orders.
*   **Supported Odoo Versions:**
    *   Integration with Mercado Pago is available from Odoo version 16 onwards for Enterprise editions.
    *   The new functionality for payments with installments is available from Odoo version 18.4 onwards.
*   **Previous Configuration Video:** A previous video on the general Mercado Pago integration configurations is already published. This video focuses specifically on installment payments, flows, and configurations.

### Flows and Configurations
*   **Module Installation:** It's important to install the `payment_mercadopago` module (payment provider for Mercado Pago). This enables the Mercado Pago payment option.
*   **Odoo Configuration:** Once the module is installed, activate and publish Mercado Pago as a payment provider in Odoo's website settings. You will need to enter your Mercado Pago access token.
*   **Mercado Pago Portal Configuration (Crucial):** This feature does *not* require additional configuration within the Odoo database for installments. Instead, the additional installment options (e.g., interest-free months, interest-based payments) must be enabled *outside of Odoo*, within your Mercado Pago portal. Instructions for accessing and configuring these options will be provided in the available resources.

### Demo: Customer Experience (Online Payment Flow)
1.  **Shopping:** A customer adds items (e.g., a cable or a box) to their cart on the Odoo e-commerce website.
2.  **Checkout:** They proceed to payment and finalize the purchase. If they are a portal user, their information (address, billing address) is pre-saved.
3.  **Invoice Option:** The system asks if the customer wants an invoice. If yes, and they've previously issued invoices as a portal user, their tax information (RFC, tax regime) is pre-saved.
4.  **Redirect to Mercado Pago:** Upon clicking "pay now," the system redirects the customer to the secure Mercado Pago portal.
5.  **Payment Method Selection:** The customer defines how they want to pay (e.g., credit card, debit card).
6.  **Installment Options (New Feature):** This is where the new functionality appears. Instead of just a single installment, customers can now see different payment options:
    *   **Single installment:** Payment in one go.
    *   **Interest-free installments:** Options like "3 months interest-free" will be displayed if configured in Mercado Pago.
    *   **Installments with interest:** Monthly payments with interest, financed by Mercado Pago.
    *   The decision to offer interest-free months is up to the company setting up the integration.
7.  **Payment Execution:** The customer selects their preferred installment option and completes the payment.
8.  **Order Confirmation:** After payment is credited, the Odoo order is confirmed (e.g., Order number 55).
9.  **Customer Portal View:** If the client has a user portal on the website, they can view their sales order management and billing information.

### Demo: Odoo Backend Experience
1.  **Automatic Sales Order Creation:** In the Odoo backend, the sales order (e.g., SO 55) is automatically created by "Odubot."
2.  **Automatic Invoice and Payment:** The billing and payment part is also automatically executed. If the client requested an invoice, it's issued.
3.  **Payment Provider Identification:** The system clearly shows that Mercado Pago is the payment provider managing this transaction.
4.  **Payment Transaction:** A payment transaction is created, associated with Mercado Pago and the Odoo company (e.g., Kemper School).

### Practical Demo Walkthrough (Specific Steps Used in Video)
The demo was performed on Odoo 18.4 using Mexico localization.
1.  **Verify Mercado Pago Setup in Odoo:**
    *   Navigate to `Website > Settings > Payment Providers`.
    *   Confirm Mercado Pago is "Active" and "Published."
    *   Ensure the Access Token is correctly entered.
2.  **Simulate a Sale:**
    *   Go to the Odoo e-commerce store.
    *   Add a product (e.g., a desk) to the cart.
    *   Proceed to payment and finalize the purchase.
    *   (As a portal user) Confirm pre-saved information.
    *   Select "Yes" to receive an invoice (RFC and tax regime pre-filled if previously used).
3.  **Perform Payment on Mercado Pago Portal:**
    *   Click "Pay Now" on the Odoo checkout page, redirecting to the Mercado Pago secure portal.
    *   Select "Credit Card" as the payment method.
    *   **Important:** Use Mercado Pago's *test cards* for demonstration purposes (different test cards exist for each country; ensure you use the correct one for your region, e.g., Mexico).
    *   Enter test card information: Visa, card number, security code, expiration date.
    *   Set the payment status to "apro" (approved payment) for testing.
    *   Choose an installment option (e.g., "three months interest-free").
    *   Complete the payment.
4.  **Verify Order Confirmation:**
    *   Observe the "Payment has already been credited" message.
    *   Note the order number (e.g., Order 55).
    *   Confirm the order is confirmed on the Odoo website.
5.  **Verify Backend Records in Odoo:**
    *   Access the Odoo backend.
    *   Locate Sales Order 55; confirm it was created by "Odubot."
    *   Verify the automatically created invoice.
    *   Check the payment transaction details, confirming Mercado Pago as the provider associated with your company.

### Available Resources
*   **Instructions for Interest-Free Months:** A link will be provided in the video description to access instructions on how to enable interest-free or interest-based payments within the Mercado Pago portal.
*   **Account/Credential Management:** Information on how to create a Mercado Pago account or manage credentials.
*   **Testing Cards:** A link to Mercado Pago's testing cards for running simulations without using real cards.

---

## Odoo 18 Tutorial: Mercado Pago Installment Payments

This tutorial outlines the steps to integrate Mercado Pago with Odoo 18 for installment payments, leveraging the new features available from Odoo 18.4 Enterprise.

**File Name Context:** `Mercado Pago - Integracion Pago con Cuotas en LATAM ｜ Odoo Configuraciones Avanzadas [YtwCbQlyzwg].vtt`

---

### Step 1: Prerequisites

*   **Odoo Version:** Ensure you are running Odoo 18.4 (or later) Enterprise edition.
*   **Mercado Pago Account:** Have an active Mercado Pago merchant account with necessary credentials (Access Token).
*   **Internet Connection:** Required for Odoo to connect with Mercado Pago.

### Step 2: Install Mercado Pago Payment Provider Module in Odoo

1.  **Navigate to Apps:** In your Odoo backend, go to the "Apps" module.
2.  **Search for Mercado Pago:** Use the search bar to find `Mercado Pago` or `payment_mercadopago`.
3.  **Install the Module:** Click the "Install" button for the "Mercado Pago Payment Acquirer" (or similar name) module.

### Step 3: Configure Mercado Pago in Odoo

1.  **Access Website Settings:** Go to the `Website` module.
2.  **Navigate to Payment Providers:** From the dashboard, go to `Configuration > Settings` (or `Website > Settings` depending on your Odoo layout). Under the "Shop" or "E-commerce" section, find "Payment Providers" and click "Manage Providers" or similar link.
3.  **Configure Mercado Pago:**
    *   Locate "Mercado Pago" in the list of payment providers.
    *   Click on it to open its settings.
    *   **Activate & Publish:** Ensure the provider is set to "Enabled" or "Active" and "Published" for your website(s).
    *   **Enter Access Token:** In the designated field (e.g., "Access Token"), paste your Mercado Pago API Access Token obtained from your Mercado Pago developer account.
    *   **Save:** Save the changes.

### Step 4: Configure Installment Options in Mercado Pago Portal (Crucial External Step)

**Important:** The installment payment options (e.g., interest-free months) are primarily configured *within your Mercado Pago merchant portal*, not directly in Odoo. Odoo simply relays the transaction to Mercado Pago, which then presents the configured installment options to the customer.

1.  **Log in to your Mercado Pago Merchant Account:** Access the Mercado Pago dashboard for sellers/developers.
2.  **Find Installment Settings:** Look for sections related to "Payments," "Checkout," "Financing," or "Installments." Mercado Pago's interface may vary, so refer to their official documentation.
3.  **Enable/Configure Installments:**
    *   You will typically find options to enable interest-free installments (`Cuotas sin interés`) or define rules for installments with interest (`Cuotas con interés`).
    *   Configure the number of installments you wish to offer (e.g., 3, 6, 12 months).
    *   Define whether you (the merchant) or the customer will bear the cost of interest.
4.  **Save Changes:** Ensure all configurations are saved in your Mercado Pago portal.

### Step 5: Simulate an E-commerce Sale and Test Installments

1.  **Access Your Odoo E-commerce Website:** Go to your Odoo website's shop page.
2.  **Add Product to Cart:** Select any product and add it to your shopping cart.
3.  **Proceed to Checkout:** Click on the cart icon and then "Proceed to Checkout" or "Process Payment."
4.  **Fill Customer Information:** If you're not logged in as a portal user, provide your shipping and billing details. If you are a portal user, verify the pre-filled information.
5.  **(Optional) Request Invoice:** If your Odoo localization supports it (e.g., Mexico), you might be prompted to request an invoice. Select "Yes" and confirm any pre-filled tax details (like RFC and tax regime).
6.  **Select Mercado Pago:** On the payment screen, choose "Mercado Pago" as your payment method.
7.  **Initiate Payment:** Click "Pay Now" or "Complete Order." You will be redirected to the secure Mercado Pago payment page.
8.  **Enter Test Card Details (for Simulation):**
    *   **Crucial:** Do NOT use a real credit card for testing. Mercado Pago provides specific [test cards](https://www.mercadopago.com/developers/en/guides/resources/testing/cards) for different countries and scenarios (approved, rejected, etc.).
    *   Select "Credit Card" as the payment type.
    *   Enter the test card number, expiration date, and security code from Mercado Pago's test card documentation.
    *   **Select Payment Status:** For successful tests, use a test card configured for "approved payment" (e.g., input "apro" in the cardholder name or status field if applicable for the test card setup).
9.  **Choose Installment Option:** This is where you will see the new feature.
    *   Observe the available installment options (e.g., "1 installment," "3 months interest-free," "monthly payments with interest").
    *   Select an installment option (e.g., "3 months interest-free").
10. **Complete Payment:** Click "Pay" on the Mercado Pago page.
11. **Verify Order Confirmation:** You will be redirected back to your Odoo website, where you should see a confirmation message indicating your payment has been credited and your order is confirmed (e.g., Order #55).

### Step 6: Verify in Odoo Backend

1.  **Access Sales Orders:** In your Odoo backend, go to the `Sales` module and then `Orders > Sales Orders`.
2.  **Locate the Order:** Find the sales order corresponding to your test purchase (e.g., SO55).
3.  **Review Order Details:**
    *   Confirm the sales order status is "Sales Order."
    *   Check the "Created by" field; it should show "Odubot," indicating it was created via the e-commerce flow.
4.  **Check Invoice and Payment:**
    *   Open the sales order.
    *   If you requested an invoice, you should see a "Customer Invoice" smart button. Click it to view the invoice. The invoice should be in "Paid" status.
    *   Look for the "Payments" smart button (or navigate to `Accounting > Payments`). You should see a payment transaction linked to the sales order.
    *   Verify that the payment transaction's provider is "Mercado Pago."

### Additional Resources:

*   **Mercado Pago Developer Documentation:** Refer to the official Mercado Pago developer documentation for the most up-to-date instructions on configuring installment options and generating access tokens.
*   **Mercado Pago Test Cards:** Always use the official [Mercado Pago test cards](https://www.mercadopago.com/developers/en/guides/resources/testing/cards) for all testing and demonstrations to avoid using real financial instruments.