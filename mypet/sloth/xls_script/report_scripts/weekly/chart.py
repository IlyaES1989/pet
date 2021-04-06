
from openpyxl.chart import (
    LineChart,
    Reference,
)
from openpyxl.chart.layout import (
    Layout,
    ManualLayout,
)
from openpyxl.chart.text import RichText
from openpyxl.drawing.text import (
    Paragraph,
    ParagraphProperties,
    CharacterProperties,
    Font,
)
from openpyxl.chart.axis import ChartLines
from openpyxl.chart.shapes import GraphicalProperties
from openpyxl.drawing.colors import ColorChoice
from openpyxl.drawing.line import LineProperties
from openpyxl.chart.legend import Legend
from openpyxl.chart.series_factory import SeriesFactory


def create_chart_sh(ws, year, title):
    last_year = year-1
    chart_sh3 = LineChart()

    last_data = Reference(ws,
                          min_col=4,
                          min_row=60,
                          max_col=15,
                          max_row=60)
    current_data = Reference(ws,
                             min_col=4,
                             min_row=63,
                             max_col=15,
                             max_row=63)

    last_series = SeriesFactory(last_data,
                                title='%s %s' % (title, last_year))
    current_series = SeriesFactory(current_data,
                                   title='%s %s' % (title, year))

    chart_sh3.series.append(last_series)
    chart_sh3.series.append(current_series)

    label = Reference(ws,
                      min_col=4,
                      min_row=3,
                      max_col=15,
                      max_row=3)
    chart_sh3.set_categories(label)

    # Charts style
    chart_sh3.width = 36
    chart_sh3.height = 6.1

    font = Font(typeface='Calibri Light')
    cp = CharacterProperties(latin=font, sz=900, solidFill='2954D6')
    line = GraphicalProperties(ln=LineProperties(w=9572, solidFill=ColorChoice(srgbClr='CED8F6')))
    axes_style = GraphicalProperties(ln=LineProperties(solidFill=ColorChoice(srgbClr='FFFFFF')))

    chart_sh3.legend = Legend(legendPos='b',
                              txPr=RichText(p=[Paragraph(pPr=ParagraphProperties(defRPr=cp), endParaRPr=cp)]))

    chart_sh3.layout = Layout(manualLayout=ManualLayout(h=0.8, w=0.97, x=0, y=0))

    chart_sh3.y_axis.majorGridlines = ChartLines(spPr=line)
    chart_sh3.y_axis.spPr = axes_style
    chart_sh3.y_axis.number_format = '0%'
    chart_sh3.y_axis.txPr = RichText(p=[Paragraph(pPr=ParagraphProperties(defRPr=cp), endParaRPr=cp)])

    chart_sh3.x_axis.txPr = RichText(p=[Paragraph(pPr=ParagraphProperties(defRPr=cp), endParaRPr=cp)])
    chart_sh3.x_axis.spPr = axes_style

    # Lines style
    s1 = chart_sh3.series[0]
    s1.marker.symbol = "circle"
    s1.marker.graphicalProperties.solidFill = "4F91C3"
    s1.marker.graphicalProperties.line.solidFill = "4F91C3"
    s1.graphicalProperties.line.solidFill = "4F91C3"
    s1.graphicalProperties.line.width = 28570

    s2 = chart_sh3.series[1]
    s2.marker.symbol = "circle"
    s2.marker.graphicalProperties.solidFill = "C00000"
    s2.marker.graphicalProperties.line.solidFill = "C00000"
    s2.graphicalProperties.line.solidFill = "C00000"
    s2.graphicalProperties.line.width = 28570

    # Entering the chart to the workbook
    ws.add_chart(chart_sh3, 'A2')
