import xlsxwriter

try:
    basestring
except NameError:
    basestring = str




x = Xlsx()
x.add_header(['DEVIS', 'S0777'])

x.add_header(['Article', 'Quantité', 'Prix unitaire'])
x.add_header([])
x.add_line(["Iphone", 3, 900.01])
x.add_line(["Ipad", 3, 200])
x.add_line(["Imac", 1, 2000])
x.add_totals()
x.add_column('Prix HT', x['Quantité'] * x['Prix unitaire'])
x.add_footer_name('XXX TOTAL XXX')
x.set_sheet('Test 6-8')
x.set_offset(6, 8)
x.add_header(['DEVIS', 'S0777'])

x.add_header(['Article', 'Quantité', 'Prix unitaire'])
x.add_header([])
x.add_line(["Iphone", 3, 900.01])
x.add_line(["Ipad", 3, 200])
x.add_line(["Imac", 1, 2000])
x.add_totals()
x.add_column('Prix HT', x['Quantité'] * x['Prix unitaire'])
x.add_footer_name('XXX TOTAL XXX')
from pprint import pprint
x.add_sheet('SANS Header')
x.add_line(["Iphone", 3, 900.01])
x.add_line(["Ipad", 3, 200])
x.add_line(["Imac", 1, 2])
x.add_totals()
x.add_sheet('SANS footer')
x.add_header(['Article', 'Quantité', 'Prix unitaire'])
x.add_line(["Iphone", 3, 900.01])
x.add_line(["Ipad", 3, 200])
x.add_line(["Imac", 1, 2])
x.add_sheet('Jsut Data')
x.add_line(["Iphone", 3, 900.01])
x.add_line(["Ipad", 3, 200])
x.add_line(["Imac", 1, 2])

x.add_sheet('Just headers')
x.add_header(['DEVIS', 'S0777'])

x.add_header(['Article', 'Quantité', 'Prix unitaire'])
x.add_header([])
x.add_sheet('Just footer')
x.add_totals()

x.add_sheet('Header + footer ')
x.add_header(['DEVIS', 'S0777'])

x.add_header(['Article', 'Quantité', 'Prix unitaire'])
x.add_header([])
x.add_totals()
x.add_footer('Article', x.SUM)

pprint(x.data)
pprint(x.data)
x.get()
