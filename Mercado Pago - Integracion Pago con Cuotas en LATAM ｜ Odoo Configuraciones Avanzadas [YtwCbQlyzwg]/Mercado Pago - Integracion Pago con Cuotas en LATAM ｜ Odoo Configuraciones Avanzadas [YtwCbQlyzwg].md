## Odoo 18 Tutorial: Mercado Pago Installment Payments in LATAM

**File Name:** `Mercado Pago - Integracion Pago con Cuotas en LATAM ｜ Odoo Configuraciones Avanzadas [YtwCbQlyzwg].vtt`

This tutorial explains how to integrate Mercado Pago installment payments into your Odoo 18 e-commerce platform, focusing on LATAM countries.  It assumes you already have the basic Mercado Pago integration set up in Odoo.

**Steps:**

1. **Odoo Version and Localization:** Ensure you are using Odoo version 18.4 or later.  Select the appropriate LATAM localization (e.g., Mexico) for your Odoo instance.  Mercado Pago installment payments are available for Mexico, Argentina, Uruguay, Peru, Colombia, Chile, and Brazil.

2. **Mercado Pago Module:**  Verify that the Mercado Pago payment provider module is installed and activated within your Odoo instance.  This module allows connection to the Mercado Pago platform.  You'll need your Mercado Pago access token to enable it.  No additional configurations are needed within the Odoo database itself; configuration happens within the Mercado Pago portal.

3. **Mercado Pago Portal Configuration (External to Odoo):**  The key configuration for installment payments is done within your Mercado Pago account.  You'll need to access your Mercado Pago portal and enable the installment payment options you want to offer. The tutorial references resources (links in video description) for enabling interest-free and interest-based installment options.

4. **Testing Your Setup (Using Test Cards):** Use Mercado Pago's test cards to simulate transactions without using real credit card information. This allows you to test the integration and various payment options thoroughly.

5. **Checkout Process:**  When a customer proceeds to checkout on your Odoo website, the system redirects them to a secure Mercado Pago page.

6. **Payment Options:** The Mercado Pago page presents multiple payment options:
    * One-time payment (single installment).
    * Interest-free installments (e.g., 3 months).
    * Installments with interest.

7. **Invoice Generation (Optional):** The customer can choose to generate an invoice during the checkout process, providing their necessary tax information (if applicable).

8. **Order and Invoice Creation in Odoo:** Once the payment is processed successfully on the Mercado Pago side, Odoo automatically creates the sales order and invoice (if selected by the customer).  Odubot handles this automatic creation.

9. **Order Management (User Portal):** The customer can then manage their orders and invoices through a user portal on your website (if you have one enabled).

10. **Backend Verification:**  After the payment, verify the sales order and invoice details within your Odoo backend.  You should find the sales order created by Odubot, and the associated invoice, payment transaction linked to Mercado Pago.


**Additional Resources:** The video mentions links in its description for:

* Instructions on setting up interest-free and interest-bearing installments on the Mercado Pago side.
* Information on creating a Mercado Pago account or managing credentials.
* Access to test credit card numbers for testing purposes.


This tutorial provides a high-level overview. Refer to the original video and the links provided in its description for detailed steps and specific configurations.
