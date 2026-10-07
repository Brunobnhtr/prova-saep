from pathlib import Path
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT
import pymupdf
from PIL import Image, ImageOps, ImageDraw

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/pdf'
OUT.mkdir(parents=True,exist_ok=True)
sets=[
('01-circuitos-resistivos','Circuitos resistivos em corrente contínua',
 'Em um resistor ideal, tensão, corrente e resistência se relacionam por V = R x I. Em série, as resistências se somam e a corrente é comum. Em paralelo, os ramos recebem a mesma tensão. Os exercícios adotam fontes ideais e desprezam a resistência dos fios.',
 [('Um resistor de 12 ohms recebe 24 V. Calcule a corrente.','I = 24 / 12 = 2 A.'),('Resistores de 10 e 20 ohms estão em série, ligados a 60 V. Determine a resistência equivalente e a corrente.','R = 10 + 20 = 30 ohms. I = 60 / 30 = 2 A.'),('No circuito anterior, qual é a tensão em cada resistor?','V1 = 10 x 2 = 20 V; V2 = 20 x 2 = 40 V. A soma é 60 V.'),('Dois resistores de 30 ohms estão em paralelo em uma fonte de 15 V. Determine a corrente de cada ramo e a corrente total.','Cada ramo conduz 15 / 30 = 0,5 A. A corrente total é 1 A; a resistência equivalente é 15 ohms.'),('Um resistor conduz 0,25 A com tensão de 10 V. Qual é sua resistência?','R = 10 / 0,25 = 40 ohms.'),('Um resistor ideal de valor constante passa de 6 para 12 V. Como varia a corrente?','A corrente dobra, pois I = V / R e R permanece constante.')]),
('02-potencia-energia','Potência e consumo de energia elétrica',
 'Potência indica a taxa de transferência de energia. Para cargas resistivas ideais, P = V x I. Energia se calcula por E = P x t. Ao usar potência em kW e tempo em horas, o resultado fica em kWh. As tarifas deste caderno são hipotéticas.',
 [('Uma carga resistiva recebe 120 V e conduz 5 A. Calcule a potência.','P = 120 x 5 = 600 W.'),('Uma lâmpada de 20 W permanece acesa por 5 horas. Qual é a energia consumida?','E = 0,020 x 5 = 0,100 kWh.'),('Um aquecedor de 2 kW funciona por 30 minutos. Qual é o consumo?','30 minutos = 0,5 hora. E = 2 x 0,5 = 1 kWh.'),('Dez lâmpadas de 12 W funcionam 8 horas por dia durante 25 dias. Determine o consumo total.','Potência total = 120 W = 0,12 kW. Tempo = 200 h. Energia = 24 kWh.'),('Com tarifa hipotética de R$ 0,80 por kWh, qual é o custo de 24 kWh?','24 x 0,80 = R$ 19,20. O exercício não inclui encargos adicionais.'),('Uma carga usa 3 kWh em 2 horas, com potência constante. Qual é a potência?','P = E / t = 3 / 2 = 1,5 kW.')]),
('03-unidades-medicoes','Unidades e interpretação de medições elétricas',
 'Os prefixos mili e quilo representam, respectivamente, um milésimo e mil unidades. Corrente se expressa em ampères, tensão em volts e resistência em ohms. Aqui, as leituras são fornecidas como dados; não são propostas atividades em circuitos reais.',
 [('Converta 250 mA para ampères.','250 / 1000 = 0,250 A.'),('Converta 4,7 kohms para ohms.','4,7 x 1000 = 4700 ohms.'),('Uma leitura é 0,008 A. Expresse em mA.','0,008 x 1000 = 8 mA.'),('Uma referência é 100 V e a leitura é 102 V. Determine o erro com sinal e o erro percentual em relação à referência.','Erro = 102 - 100 = +2 V. Percentual = 2 / 100 x 100 = +2%.'),('As leituras são 10,1 V, 10,2 V e 10,3 V. Determine a média.','Média = (10,1 + 10,2 + 10,3) / 3 = 10,2 V.'),('Um indicador exibe 1,25 kW. Expresse esse valor em watts.','1,25 x 1000 = 1250 W.')]),
('04-logica-comandos','Lógica booleana aplicada a comandos',
 'Neste modelo didático, 1 representa condição verdadeira e 0 representa falsa. A operação E só resulta em 1 quando todas as entradas são 1. A operação OU resulta em 1 quando ao menos uma entrada é 1. NÃO inverte a entrada. São modelos lógicos, sem dimensionamento ou projeto de segurança.',
 [('Calcule A E B para A = 1 e B = 0.','Resultado 0: uma das condições não está satisfeita.'),('Calcule A OU B para A = 0 e B = 1.','Resultado 1: existe uma entrada verdadeira.'),('Calcule NÃO A para A = 0.','Resultado 1.'),('Uma saída obedece a S = A E B. Liste os resultados para 00, 01, 10 e 11.','Na ordem solicitada: 0, 0, 0, 1.'),('Uma saída obedece a S = (A OU B) E C. Avalie A = 0, B = 1 e C = 0.','A OU B = 1. Depois 1 E 0 = 0. Portanto S = 0.'),('No mesmo modelo, avalie A = 1, B = 0 e C = 1.','A OU B = 1. Depois 1 E 1 = 1. Portanto S = 1.')]),
('05-transformadores-ideais','Relações de um transformador ideal',
 'Para um transformador monofásico ideal em regime alternado, Vp / Vs = Np / Ns. A potência é conservada no modelo: Vp x Ip = Vs x Is. São usadas cargas com fator de potência unitário. As relações ignoram perdas, impedâncias e limites térmicos.',
 [('Um transformador tem 1000 espiras no primário e 200 no secundário. Com 230 V no primário, qual é a tensão secundária?','Vs = 230 x 200 / 1000 = 46 V.'),('Para obter 24 V a partir de 240 V, qual deve ser a razão Np / Ns?','Np / Ns = 240 / 24 = 10.'),('Uma carga secundária de 24 V conduz 5 A. Calcule a potência no modelo adotado.','P = 24 x 5 = 120 W.'),('O primário do caso anterior recebe 240 V. Qual é a corrente primária ideal?','Ip = 120 / 240 = 0,5 A.'),('Um primário tem 600 espiras. A relação de tensão é 120 V para 30 V. Quantas espiras tem o secundário?','Ns = 600 x 30 / 120 = 150 espiras.'),('Ao reduzir a tensão de 200 V para 50 V mantendo a potência ideal, como varia a corrente?','A tensão cai por um fator 4. A corrente secundária é quatro vezes a primária, preservando o produto V x I.')])]
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='CoverTitle',fontName='Helvetica-Bold',fontSize=23,leading=28,textColor=HexColor('#123642'),spaceAfter=20))
styles.add(ParagraphStyle(name='BodyCustom',fontSize=11,leading=16,spaceAfter=13))
styles.add(ParagraphStyle(name='SmallCustom',fontSize=9,leading=13,textColor=HexColor('#52636b'),spaceAfter=14))
def footer(c,d):
    c.setStrokeColor(HexColor('#ccd6da')); c.line(48,43,547,43)
    c.setFont('Helvetica',8); c.setFillColor(HexColor('#52636b'))
    c.drawString(48,29,'Caderno original de estudo | Eletrotécnica | Material independente')
    c.drawRightString(547,29,str(d.page))
thumbs=[]
for slug,title,intro,exercises in sets:
    file=OUT/(slug+'.pdf')
    story=[Paragraph('CADERNO DE EXERCÍCIOS',styles['SmallCustom']),Paragraph(title,styles['CoverTitle']),Paragraph('Material original elaborado com auxílio de IA para estudo individual. Não é publicação oficial do SENAI nem prova SAEP. Exercícios e soluções criados para esta coleção, sem reprodução dos livros ou das provas do acervo.',styles['SmallCustom']),Paragraph('Conceitos e hipóteses',styles['Heading2']),Paragraph(intro,styles['BodyCustom']),Paragraph('Exercícios',styles['Heading2'])]
    for i,(q,a) in enumerate(exercises,1):
        story.extend([Paragraph(f'<b>{i}.</b> {q}',styles['BodyCustom']),Spacer(1,8)])
    story.extend([PageBreak(),Paragraph('Soluções comentadas',styles['CoverTitle']),Paragraph('Compare o resultado, a unidade e o raciocínio. Refaça os cálculos antes de consultar cada solução.',styles['BodyCustom'])])
    for i,(q,a) in enumerate(exercises,1): story.append(Paragraph(f'<b>{i}.</b> {a}',styles['BodyCustom']))
    story.extend([Spacer(1,18),Paragraph('Revisão pessoal',styles['Heading2']),Paragraph('Anote qual etapa apresentou dificuldade, refaça o exercício com outros valores e confira se o resultado respeita as hipóteses do modelo.',styles['BodyCustom'])])
    SimpleDocTemplate(str(file),pagesize=(595.28,841.89),rightMargin=48,leftMargin=48,topMargin=48,bottomMargin=60,title=title,author='Material de estudo independente').build(story,onFirstPage=footer,onLaterPages=footer)
    with pymupdf.open(file) as doc:
        assert len(doc)==2,(slug,len(doc))
        for page in doc:
            assert page.get_text().strip()
            pix=page.get_pixmap(matrix=pymupdf.Matrix(0.7,0.7))
            img=Image.frombytes('RGB',[pix.width,pix.height],pix.samples)
            thumbs.append(img)
qa=ROOT/'tmp/pdfs';qa.mkdir(parents=True,exist_ok=True)
sheet=Image.new('RGB',(thumbs[0].width*5,thumbs[0].height*2),'#dddddd')
for i,img in enumerate(thumbs): sheet.paste(img,((i//2)*img.width,(i%2)*img.height))
sheet.save(qa/'cinco-cadernos-contato.png')
print('5 PDFs criados, 2 páginas e 6 exercícios com soluções por documento.')
