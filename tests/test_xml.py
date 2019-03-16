from unittest import TestCase


class TestXML(TestCase):
    def test_load_data(self):
        from dyools import XML
        arch = """
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
        self.assertIsNotNone(XML(arch))
        self.assertEqual(XML(arch).xpath('extra'), [b'<extra>1</extra>', b'<extra>2</extra>'])
        self.assertEqual(XML(arch).xpath(name='phone'), [b'<field name="phone"/>'])
        self.assertEqual(XML(arch).xpath(name='email'),
                         [b'<field name="email"/>', b'<field name="email" widget="email"/>'])
        self.assertEqual(XML(arch).xpath('field', name='email'),
                         [b'<field name="email"/>', b'<field name="email" widget="email"/>'])
        self.assertEqual(XML(arch).xpath('field', name='email', widget='email'),
                         [b'<field name="email" widget="email"/>'])

    def test_xml_separator_1(self):
        from dyools import XML
        arch = """
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
        self.assertEqual(len(XML(arch, separator='====').all_nodes()), 1)

    def test_xml_separator_2(self):
        from dyools import XML
        arch = """
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
        self.assertEqual(len(XML(arch, separator='====').all_nodes()), 6)
