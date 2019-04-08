from unittest import TestCase


class TestXML(TestCase):
    def setUp(self):
        self.big_xml = """
        <form string="Bon de commande" class="o_sale_order">
                <header>
                    <field name="authorized_transaction_ids" invisible="1"/>
                    <button name="payment_action_capture" type="object" string="Capturer la transaction" class="oe_highlight" attrs="{'invisible': [('authorized_transaction_ids', '=', [])]}"/>
                    <button name="payment_action_void" type="object" string="Annuler la transaction" confirm="Are you sure you want to void the authorized transaction? This action can't be undone." attrs="{'invisible': [('authorized_transaction_ids', '=', [])]}"/>
                    <button name="action_quotation_send" string="Envoyer par email" type="object" states="draft" class="btn-primary"/>
                    <button name="action_quotation_send" type="object" string="Envoyer la facture PRO FORMA" groups="sale.group_proforma_sales" class="btn-primary" attrs="{'invisible': ['|', ('state', '!=', 'draft'), ('invoice_count','&gt;=',1)]}" context="{'proforma': True}"/>
                    <button name="print_quotation" string="Imprimer" type="object" states="draft" class="btn-primary o_sale_print"/>
                    <button name="action_confirm" id="action_confirm" string="Confirmer" class="btn-primary" type="object" attrs="{'invisible': [('state', 'not in', ['sent'])]}"/>
                    <button name="action_confirm" string="Confirmer" type="object" attrs="{'invisible': [('state', 'not in', ['draft'])]}"/>
                    <button name="preview_sale_order" type="object" string="Prévisualiser"/>
                    <button name="action_quotation_send" type="object" string="Envoyer la facture PRO FORMA" groups="sale.group_proforma_sales" attrs="{'invisible': ['|', ('state', '=', 'draft'), ('invoice_count','&gt;=',1)]}" context="{'proforma': True}"/>
                    <button name="print_quotation" string="Imprimer" type="object" states="sent,sale" class="o_sale_print"/>
                    <button name="action_quotation_send" string="Envoyer par email" type="object" states="sent,sale"/>
                    <button name="action_cancel" states="draft,sent,sale" type="object" string="Annuler"/>
                    <button name="action_draft" states="cancel" type="object" string="Mettre en Devis"/>
                    <button name="action_done" type="object" string="Bloquer" states="sale" help="Si la vente est verrouillée, vous ne pouvez plus la modifier. Toutefois, vous pourrez toujours facturer ou expédier."/>
                    <button name="action_unlock" type="object" string="Déverrouiller" states="done" groups="sales_team.group_sale_manager"/>
                    <field name="state" widget="statusbar" statusbar_visible="draft,sent,sale"/>
                </header>
                <sheet>
                    <div class="oe_button_box" name="button_box">
                        <button name="action_view_invoice" type="object" class="oe_stat_button" icon="fa-pencil-square-o" attrs="{'invisible': [('invoice_count', '=', 0)]}">
                            <field name="invoice_count" widget="statinfo" string="Factures"/>
                        </button>
                    </div>
                    <div class="oe_title">
                        <h1>
                            <field name="name" readonly="1"/>
                        </h1>
                    </div>
                    <group>
                        <group>
                            <field name="partner_id" widget="res_partner_many2one" domain="[('customer','=',True)]" context="{'search_default_customer':1, 'show_address': 1, 'show_vat': True}" options="{&quot;always_reload&quot;: True}"/>
                            <field name="partner_invoice_id" groups="sale.group_delivery_invoice_address" context="{'default_type':'invoice'}" options="{&quot;always_reload&quot;: True}"/>
                            <field name="partner_shipping_id" groups="sale.group_delivery_invoice_address" context="{'default_type':'delivery'}" options="{&quot;always_reload&quot;: True}"/>
                        </group>
                        <group>
                            <field name="validity_date" attrs="{'invisible': [('state', 'in', ['sale', 'done'])]}"/>
                            <field name="confirmation_date" attrs="{'invisible': [('state', 'in', ['draft', 'sent', 'cancel'])]}"/>
                            <field name="pricelist_id" groups="product.group_sale_pricelist"/>
                            <field name="currency_id" invisible="1"/>
                            <field name="payment_term_id" options="{'no_create': True}"/>
                        </group>
                    </group>
                    <notebook>
                        <page string="Lignes de la commande" name="order_lines">
                            <field name="order_line" widget="section_and_note_one2many" mode="tree,kanban" attrs="{'readonly': [('state', 'in', ('done','cancel'))]}">
                                <form>
                                    <field name="display_type" invisible="1"/>
                                    <!--
                                        We need the sequence field to be here for new lines to be added at the correct position.
                                        TODO: at some point we want to fix this in the framework so that an invisible field is not required.
                                    -->
                                    <field name="sequence" invisible="1"/>
                                    <group>
                                        <group attrs="{'invisible': [('display_type', '!=', False)]}">
                                            <field name="product_updatable" invisible="1"/>
                                            <field name="product_id" context="{'partner_id':parent.partner_id, 'quantity':product_uom_qty, 'pricelist':parent.pricelist_id, 'uom':product_uom, 'company_id': parent.company_id}" attrs="{                                                     'readonly': [('product_updatable', '=', False)],                                                     'required': [('display_type', '=', False)],                                                 }" force_save="1"/>
                                            <field name="invoice_status" invisible="1"/>
                                            <field name="qty_to_invoice" invisible="1"/>
                                            <field name="qty_delivered_manual" invisible="1"/>
                                            <field name="qty_delivered_method" invisible="1"/>
                                            <field name="price_total" invisible="1"/>
                                            <field name="price_tax" invisible="1"/>
                                            <field name="price_subtotal" invisible="1"/>
                                            <label for="product_uom_qty" string="Quantité commandée"/>
                                            <div>
                                                <field context="{'partner_id':parent.partner_id, 'quantity':product_uom_qty, 'pricelist':parent.pricelist_id, 'uom':product_uom, 'uom_qty_change':True, 'company_id': parent.company_id}" name="product_uom_qty" class="oe_inline"/>
                                                <field name="product_uom" force_save="1" groups="uom.group_uom" class="oe_inline oe_no_button" attrs="{                                                         'readonly': [('state', 'in', ('sale', 'done', 'cancel'))],                                                         'required': [('display_type', '=', False)],                                                     }"/>
                                            </div>
                                            <label for="qty_delivered" string="Qté livrée" attrs="{'invisible': [('parent.state', 'not in', ['sale', 'done'])]}"/>
                                            <div attrs="{'invisible': [('parent.state', 'not in', ['sale', 'done'])]}">
                                                <field name="qty_delivered" attrs="{'readonly': [('qty_delivered_method', '!=', 'manual')]}"/>
                                            </div>
                                            <label for="qty_invoiced" string="Quantité facturée" attrs="{'invisible': [('parent.state', 'not in', ['sale', 'done'])]}"/>
                                            <div attrs="{'invisible': [('parent.state', 'not in', ['sale', 'done'])]}">
                                                <field name="qty_invoiced" attrs="{'invisible': [('parent.state', 'not in', ['sale', 'done'])]}"/>
                                            </div>
                                            <field name="price_unit"/>
                                            <label for="discount" groups="sale.group_discount_per_so_line"/>
                                            <div name="discount" groups="sale.group_discount_per_so_line">
                                                <field name="discount" class="oe_inline"/> %
                                            </div>
                                            <!--
                                                We need the sequence field to be here
                                                because we want to be able to overwrite the default sequence value in the JS
                                                in order for new lines to be added at the correct position.
                                                NOTE: at some point we want to fix this in the framework so that an invisible field is not required.
                                            -->
                                            <field name="sequence" invisible="1"/>
                                        </group>
                                        <group attrs="{'invisible': [('display_type', '!=', False)]}">
                                            <field name="tax_id" widget="many2many_tags" options="{'no_create': True}" context="{'search_view_ref': 'account.account_tax_view_search'}" domain="[('type_tax_use','=','sale'),('company_id','=',parent.company_id)]" attrs="{'readonly': [('qty_invoiced', '&gt;', 0)]}"/>
                                            <label for="customer_lead"/>
                                            <div>
                                                <field name="customer_lead" class="oe_inline"/> jours
                                            </div>
                                            <label for="analytic_tag_ids" groups="analytic.group_analytic_tags"/>
                                            <div>
                                                <field name="analytic_tag_ids" widget="many2many_tags" groups="analytic.group_analytic_tags" options="{'color_field': 'color'}"/>
                                            </div>
                                        </group>
                                    </group>
                                    <label for="name" string="Description" attrs="{'invisible': [('display_type', '!=', False)]}"/>
                                    <label for="name" string="Nom de section (e.g. Articles, Services)" attrs="{'invisible': [('display_type', '!=', 'line_section')]}"/>
                                    <label for="name" string="Note" attrs="{'invisible': [('display_type', '!=', 'line_note')]}"/>
                                    <field name="name"/>
                                    <div groups="base.group_no_one" attrs="{'invisible': [('display_type', '!=', False)]}">
                                        <label for="invoice_lines"/>
                                        <field name="invoice_lines"/>
                                    </div>
                                    <field name="state" invisible="1"/>
                                </form>
                                <!-- This is inherited below to make the order lines non-editable (inline)
                                    for the members of some usability groups (packaging, event):
                                    Indeed in those cases we need a dialog because there are additional fields to input.
                                -->
                                <tree string="Lignes de bons de commande" editable="bottom" decoration-info="(not display_type and invoice_status == 'to invoice')">
                                    <control>
                                        <create string="Ajouter un produit"/>
                                        <create string="Configurez un article" context="{'open_product_configurator': True}" groups="product.group_product_variant"/>
                                        <create string="Ajouter une section" context="{'default_display_type': 'line_section'}"/>
                                        <create string="Ajouter une note" context="{'default_display_type': 'line_note'}"/>
                                    </control>

                                    <field name="sequence" widget="handle"/>
                                    <!-- We do not display the type because we don't want the user to be bothered with that information if he has no section or note. -->
                                    <field name="display_type" invisible="1"/>

                                    <field name="product_updatable" invisible="1"/>
                                    <field name="product_id" attrs="{                                             'readonly': [('product_updatable', '=', False)],                                             'required': [('display_type', '=', False)],                                         }" force_save="1" context="{                                             'partner_id': parent.partner_id,                                             'quantity': product_uom_qty,                                             'pricelist': parent.pricelist_id,                                             'uom':product_uom,                                             'company_id': parent.company_id,                                             'default_lst_price': price_unit,                                             'default_description_sale': name                                         }"/>
                                    <field name="product_custom_attribute_value_ids" invisible="1"/>
                                    <field name="product_no_variant_attribute_value_ids" invisible="1"/>
                                    <field name="name" widget="section_and_note_text"/>
                                    <field name="product_uom_qty" string="Qté commandée" context="{                                             'partner_id': parent.partner_id,                                             'quantity': product_uom_qty,                                             'pricelist': parent.pricelist_id,                                             'uom': product_uom,                                             'company_id': parent.company_id                                         }"/>
                                    <field name="qty_delivered" attrs="{                                             'column_invisible': [('parent.state', 'not in', ['sale', 'done'])],                                             'readonly': [('qty_delivered_method', '!=', 'manual')]                                         }"/>
                                    <field name="qty_delivered_manual" invisible="1"/>
                                    <field name="qty_delivered_method" invisible="1"/>
                                    <field name="qty_invoiced" attrs="{'column_invisible': [('parent.state', 'not in', ['sale', 'done'])]}"/>
                                    <field name="qty_to_invoice" invisible="1"/>
                                    <field name="product_uom" force_save="1" attrs="{                                             'readonly': [('state', 'in', ('sale','done', 'cancel'))],                                             'required': [('display_type', '=', False)],                                         }" context="{'company_id': parent.company_id}" groups="uom.group_uom" options="{&quot;no_open&quot;: True}"/>
                                    <field name="analytic_tag_ids" groups="analytic.group_analytic_tags" widget="many2many_tags"/>
                                    <field name="price_unit" attrs="{'readonly': [('qty_invoiced', '&gt;', 0)]}"/>
                                    <field name="tax_id" widget="many2many_tags" options="{'no_create': True}" domain="[('type_tax_use','=','sale'),('company_id','=',parent.company_id)]" attrs="{'readonly': [('qty_invoiced', '&gt;', 0)]}"/>
                                    <field name="discount" groups="sale.group_discount_per_so_line"/>
                                    <field name="price_subtotal" widget="monetary" groups="account.group_show_line_subtotals_tax_excluded"/>
                                    <field name="price_total" widget="monetary" groups="account.group_show_line_subtotals_tax_included"/>
                                    <field name="state" invisible="1"/>
                                    <field name="invoice_status" invisible="1"/>
                                    <field name="customer_lead" invisible="1"/>
                                    <field name="currency_id" invisible="1"/>
                                    <field name="price_tax" invisible="1"/>
                                </tree>
                                <kanban class="o_kanban_mobile">
                                    <field name="name"/>
                                    <field name="product_id"/>
                                    <field name="product_uom_qty"/>
                                    <field name="product_uom" groups="uom.group_uom"/>
                                    <field name="price_subtotal"/>
                                    <field name="price_tax" invisible="1"/>
                                    <field name="price_total" invisible="1"/>
                                    <field name="price_unit"/>
                                    <field name="display_type"/>
                                    <templates>
                                        <t t-name="kanban-box">
                                            <div t-attf-class="oe_kanban_card oe_kanban_global_click {{ record.display_type.raw_value ? 'o_is_' + record.display_type.raw_value : '' }}">
                                                <t t-if="!record.display_type.raw_value">
                                                    <div class="row">
                                                        <div class="col-8">
                                                            <strong>
                                                                <span>
                                                                    <t t-esc="record.product_id.value"/>
                                                                </span>
                                                            </strong>
                                                        </div>
                                                        <div class="col-4">
                                                            <strong>
                                                                <span class="float-right text-right">
                                                                    <t t-esc="record.price_subtotal.value"/>
                                                                </span>
                                                            </strong>
                                                        </div>
                                                    </div>
                                                    <div class="row">
                                                        <div class="col-12 text-muted">
                                                            <span>
                                                                Quantité:
                                                                <t t-esc="record.product_uom_qty.value"/>
                                                                <t t-esc="record.product_uom.value"/>
                                                            </span>
                                                        </div>
                                                    </div>
                                                    <div class="row">
                                                        <div class="col-12 text-muted">
                                                            <span>
                                                                Prix de l'unité :
                                                                <t t-esc="record.price_unit.value"/>
                                                            </span>
                                                        </div>
                                                    </div>
                                                </t>
                                                <t t-if="record.display_type.raw_value === 'line_section' || record.display_type.raw_value === 'line_note'">
                                                    <div class="row">
                                                        <div class="col-12">
                                                            <span>
                                                                <t t-esc="record.name.value"/>
                                                            </span>
                                                        </div>
                                                    </div>
                                                </t>
                                            </div>
                                        </t>
                                    </templates>
                                </kanban>
                            </field>
                            <group class="oe_subtotal_footer oe_right" colspan="2" name="sale_total">
                                <field name="amount_untaxed" widget="monetary" options="{'currency_field': 'currency_id'}"/>
                                <field name="amount_tax" widget="monetary" options="{'currency_field': 'currency_id'}"/>
                                <div class="oe_subtotal_footer_separator oe_inline o_td_label">
                                    <label for="amount_total"/>
                                </div>
                                <field name="amount_total" nolabel="1" class="oe_subtotal_footer_separator" widget="monetary" options="{'currency_field': 'currency_id'}"/>
                            </group>
                            <field name="note" class="oe_inline" placeholder="Termes et conditions... (note: vous pouvez définir ceux par défaut dans le menu Configuration)"/>
                            <div class="oe_clear"/>
                        </page>
                        <page string="Autres informations" name="other_information">
                            <group>
                                <group string="Informations de livraison" name="sale_shipping" groups="sale.group_sale_order_dates">
                                    <field name="expected_date" groups="sale.group_sale_order_dates"/>
                                    <field name="commitment_date" groups="sale.group_sale_order_dates"/>
                                </group>
                                <group string="Information sur les ventes" name="sales_person">
                                    <field name="user_id"/>
                                    <field name="team_id" options="{'no_create': True}"/>
                                    <field name="client_order_ref"/>
                                    <field name="require_signature"/>
                                    <field name="require_payment"/>
                                    <field name="reference" readonly="1" attrs="{'invisible': [('reference', '=', False)]}"/>
                                    <field name="company_id" options="{'no_create': True}" groups="base.group_multi_company"/>
                                    <field name="analytic_account_id" context="{'default_partner_id':partner_invoice_id, 'default_name':name}" attrs="{'readonly': [('invoice_count','!=',0),('state','=','sale')]}" groups="analytic.group_analytic_accounting" force_save="1"/>
                                </group>
                                <group name="sale_pay" string="Facturation">
                                    <field name="date_order" attrs="{'invisible': [('state', 'in', ['sale', 'done', 'cancel'])]}"/>
                                    <field name="fiscal_position_id" options="{'no_create': True}"/>
                                    <field name="invoice_status" states="sale,done" invisible="1"/>
                                </group>
                                <group string="Analyse" name="technical" groups="base.group_no_one">
                                    <field groups="base.group_no_one" name="origin"/>
                                </group>
                                <group name="utm_link" groups="base.group_no_one"/>
                            </group>
                        </page>
                    </notebook>
                </sheet>
                <div class="oe_chatter">
                    <field name="message_follower_ids" widget="mail_followers"/>
                    <field name="activity_ids" widget="mail_activity"/>
                    <field name="message_ids" widget="mail_thread"/>
                </div>
                </form>

        """
        self.small_xml = """
        <form string="Bank">
                <extra>1</extra>
                <extra>2</extra>
                <group col="4">
                    <field name="name"/>
                    <field name="bic"/>
                </group>
                <group name="simple_group">
                    <group string="Address">
                        <label for="street" string="Address"/>
                        <div class="o_address_format">
                            <field name="street" placeholder="Street..." class="o_address_street"/>
                            <field name="street2" placeholder="Street 2..." class="o_address_street"/>
                            <field name="city" placeholder="City" class="o_address_city"/>
                            <field name="state" class="o_address_state" placeholder="State" options="{&quot;no_open&quot;: True}"/>
                            <field name="zip" placeholder="ZIP" class="o_address_zip"/>
                            <field name="country" placeholder="Country" class="o_address_country" options="{&quot;no_open&quot;: True, &quot;no_create&quot;: True}"/>
                        </div>
                    </group>
                    <group string="Communication" name="communication">
                        <field name="phone"/>
                        <field name="email"/>
                        <field name="email" widget="email"/>
                        <field name="active"/>
                        <field name="active"/>
                    </group>
                </group>
            </form>
            """
        self.separator_xml1 = """
            <form string="Bank">
                <extra>1</extra>
                <extra>2</extra>
                <group col="4">
                    <field name="name"/>
                    <field name="bic"/>
                </group>
                <group name="simple_group">
                    <group string="Address">
                        <label for="street" string="Address"/>
                        <div class="o_address_format">
                            <field name="street" placeholder="Street..." class="o_address_street"/>
                            <field name="street2" placeholder="Street 2..." class="o_address_street"/>
                            <field name="city" placeholder="City" class="o_address_city"/>
                            <field name="state" class="o_address_state" placeholder="State" options="{&quot;no_open&quot;: True}"/>
                            <field name="zip" placeholder="ZIP" class="o_address_zip"/>
                            <field name="country" placeholder="Country" class="o_address_country" options="{&quot;no_open&quot;: True, &quot;no_create&quot;: True}"/>
                        </div>
                    </group>
                    <group string="Communication" name="communication">
                        <field name="phone"/>
                    ====
                        <field name="email"/>
                    ====
                        <field name="email" widget="email"/>
                        <field name="active"/>
                        <field name="active"/>
                    </group>
                </group>
            </form>

        """
        self.separator_xml2 = """
            <form string="Bank">
                <extra>1</extra>
                <extra>2</extra>
                <group col="4">
                    <field name="name"/>
                    <field name="bic"/>
                </group>
                <group name="simple_group">
                    <group string="Address">
                        <label for="street" string="Address"/>
                        <div class="o_address_format">
                            <field name="street" placeholder="Street..." class="o_address_street"/>
                            <field name="street2" placeholder="Street 2..." class="o_address_street"/>
                            <field name="city" placeholder="City" class="o_address_city"/>
                            <field name="state" class="o_address_state" placeholder="State" options="{&quot;no_open&quot;: True}"/>
                            <field name="zip" placeholder="ZIP" class="o_address_zip"/>
                            <field name="country" placeholder="Country" class="o_address_country" options="{&quot;no_open&quot;: True, &quot;no_create&quot;: True}"/>
                        </div>
                    </group>
                    ====
                    <group string="Communication" name="communication">
                        <field name="phone"/>
                        <field name="email"/>
                        <field name="email" widget="email"/>
                        <field name="active"/>
                        <field name="active"/>
                    </group>
                    ====
                </group>
            </form>

        """

    def test_load_data(self):
        from dyools import Xml
        arch = self.small_xml
        self.assertIsNotNone(Xml(arch))
        self.assertEqual(Xml(arch).xpath('extra'), [b'<extra>1</extra>', b'<extra>2</extra>'])
        self.assertEqual(Xml(arch).xpath(name='phone'), [b'<field name="phone"/>'])
        self.assertEqual(Xml(arch).xpath(name='email'),
                         [b'<field name="email"/>', b'<field name="email" widget="email"/>'])
        self.assertEqual(Xml(arch).xpath('field', name='email'),
                         [b'<field name="email"/>', b'<field name="email" widget="email"/>'])
        self.assertEqual(Xml(arch).xpath('field', name='email', widget='email'),
                         [b'<field name="email" widget="email"/>'])

    def test_xml_separator_1(self):
        from dyools import Xml
        arch = self.separator_xml1
        self.assertEqual(len(Xml(arch, separator='====').all_nodes()), 1)

    def test_xml_separator_2(self):
        from dyools import Xml
        arch = self.separator_xml2
        self.assertEqual(len(Xml(arch, separator='====').all_nodes()), 6)

    def test_xml_query(self):
        from dyools import Xml
        xml = Xml(self.big_xml)

