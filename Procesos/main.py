import numpy as np
from time import sleep
from bokeh.document import Document
from bokeh.models import ColumnDataSource , PreText
from bokeh.layouts import layout
from bokeh.plotting import curdoc , figure
from bokeh.models.widgets import RadioButtonGroup, TextInput, Select, Button
from threading import Thread
import pandas as pd
from opcua import ua
from opcua import Client
from connection import GetConnection


class UpdateLectura(Thread):
	def __init__(self,lectura):
		Thread.__init__(self)
		self.lectura = lectura

	def run(self):
		while(1):
			#print('Running')
			sleep(1)
			for x in lectura:
				lectura[x]+=1
				if(lectura[x]>10):
					lectura[x] = 0.0



lectura = {'t1':1.0,'t2':1.0,'t3':1.0,'t4':1.0,'nu1':1.0,'nu2':1.0,'ng1':1.0, 'ng2':1.0}
inputs = dict(v1=1.0,v2=1.0,r1=1.0,r2=1.0,kp=1.0,ki=0.0,kd=0.0,h1=1.0,h2=1.0)
#connections = GetConnection()

def SetValues(new_u1,new_u2):
	global connections
	connections['u1'] = new_u1
	connections['u2'] = new_u2

def GetValues():
	global connections, lectura
	u1 = round(connections['u1'].get_value(),2)
	u2 = round(connections['u2'].get_value(),2)
	g1 = round(connections['g1'].get_value(),2)
	g2 = round(connections['g2'].get_value(),2)
	t1 = round(connections['t1'].get_value(),2)
	t2 = round(connections['t2'].get_value(),2)
	t3 = round(connections['t3'].get_value(),2)
	t4 = round(connections['t4'].get_value(),2)
	lectura = dict(nu1=u1,nu2=u2,ng1=g1,ng2=g2,t1=t1,t2=t2,t3=t3,t4=t4)

def Save(saving, save_to, data_saved):
	if (saving==1):
		data_saved = ColumnDataSource(dict(time=[],mode=[],t1=[],t2=[],t3=[],t4=[],nu1=[],nu2=[],kp=[],ki=[],kd=[],r1=[],r2=[],h1=[],h2=[]))
	if (saving==0):
		data_frame = data_saved.to_df()
		if(save_to == 'csv'):
			data_frame.to_csv('Procesos/saved.csv')
		elif(save_to == 'npy'):
			to_save = data_frame.values
			np.save('Procesos/saved.npy', to_save)
		elif(save_to == 'txt'):
			np.savetxt('Procesos/saved.txt', data_frame.values, fmt='%s', delimiter=', ')


def Saving(data_saved, manual):
	update = dict(time=[t], 
		nu1=[lectura['nu1']], 
		nu2=[lectura['nu2']], 
		t1=[lectura['t1']], 
		t2=[lectura['t2']],
		t3=[lectura['t3']],
		t4=[lectura['t4']],
		h1=[float(h1_text.value)],
		h2=[float(h2_text.value)],
		kp=[float(kp_text.value)],
		ki=[float(ki_text.value)],
		kd=[float(kd_text.value)],
		r1=[float(r1_text.value)],
		r2=[float(r2_text.value)]
		)
	if(manual==1):
		update['kp'] = ['-']
		update['ki'] = ['-']
		update['kd'] = ['-']
		update['h1'] = ['-']
		update['h2'] = ['-']
		update['mode'] = ['M']
	else:
		update['mode'] = ['A']
	data_saved.stream(new_data=update)





def Mode(manual):
	if(manual==0):
		v1_text.disabled = True
		v2_text.disabled = True
		r1_text.disabled = True
		r2_text.disabled = True
		h1_text.disabled = False
		h2_text.disabled = False
		h1_line.visible = True
		h2_line.visible = True
		kp_text.disabled = False
		ki_text.disabled = False
		kd_text.disabled = False
		compi_text.disabled = False
		compd_text.disabled = False

	else:
		v1_text.disabled = False
		v2_text.disabled = False
		r1_text.disabled = False
		r2_text.disabled = False
		h1_text.disabled = True
		h2_text.disabled = True
		h1_line.visible = False
		h2_line.visible = False
		kp_text.disabled = True
		ki_text.disabled = True
		kd_text.disabled = True
		compi_text.disabled = True
		compd_text.disabled = True

# Se c r e a un sen o
T = np.linspace(0 , 1000 , 1001)

 # Se c r e a e l DataSource
data = ColumnDataSource(dict(time=[], nu1=[], nu2=[], t1=[], t2=[], t3=[], t4=[], h1=[], h2=[]))
data_saved = ColumnDataSource(dict(time=[],mode=[],t1=[],t2=[],t3=[],t4=[],nu1=[],nu2=[],kp=[],ki=[],kd=[],r1=[],r2=[],h1=[],h2=[]))
# Fi gu r a voltaje valvula 1
fig_u1=figure(title='Voltaje Valvula 1', plot_width=600, plot_height=200, tools='reset,xpan,xwheel_zoom,xbox_zoom', y_axis_location='left')
fig_u1.line(x='time',y='nu1', alpha=0.8, line_width=3,color='blue', source=data, legend='U1')
fig_u1.xaxis.axis_label = 'Tiempo (S)'
fig_u1.yaxis.axis_label = 'Valores'

# Figura voltaje valvula 2
fig_u2=figure(title='Voltaje Valvula 2', plot_width=600, plot_height=200, tools='reset,xpan,xwheel_zoom,xbox_zoom', y_axis_location='left')
fig_u2.line(x='time',y='nu2', alpha=0.8, line_width=3,color='blue', source=data, legend='U2')
fig_u2.xaxis.axis_label = 'Tiempo (S)'
fig_u2.yaxis.axis_label = 'Valores'

#Figura altura tanque 1
fig_t1=figure(title='Altura tanque 1', plot_width=600, plot_height=200, tools='reset,xpan,xwheel_zoom,xbox_zoom', y_axis_location='left')
fig_t1.line(x='time',y='t1', alpha=0.8, line_width=3,color='red', source=data, legend='T1')
h1_line = fig_t1.line(x='time',y='h1', alpha=0.8, line_width=3, color='black', source=data, legend='H1')
fig_t1.xaxis.axis_label = 'Tiempo (S)'
fig_t1.yaxis.axis_label = 'Valores'

#figura altura tanque 2
fig_t2=figure(title='Altura tanque 2', plot_width=600, plot_height=200, tools='reset,xpan,xwheel_zoom,xbox_zoom', y_axis_location='left')
fig_t2.line(x='time',y='t2', alpha=0.8, line_width=3,color='red', source=data, legend='T2')
h2_line = fig_t2.line(x='time',y='h2', alpha=0.8, line_width=3, color='black', source=data, legend='H2')
fig_t2.xaxis.axis_label = 'Tiempo (S)'
fig_t2.yaxis.axis_label = 'Valores'

#figura altura tanque 3
fig_t3=figure(title='Altura tanque 3', plot_width=600, plot_height=200, tools='reset,xpan,xwheel_zoom,xbox_zoom', y_axis_location='left')
fig_t3.line(x='time',y='t3', alpha=0.8, line_width=3,color='green', source=data, legend='T3')
fig_t3.xaxis.axis_label = 'Tiempo (S)'
fig_t3.yaxis.axis_label = 'Valores'

#figura altura tanque 4
fig_t4=figure(title='Altura tanque 4', plot_width=600, plot_height=200, tools='reset,xpan,xwheel_zoom,xbox_zoom', y_axis_location='left')
fig_t4.line(x='time',y='t4', alpha=0.8, line_width=3,color='green', source=data, legend='T4')
fig_t4.xaxis.axis_label = 'Tiempo (S)'
fig_t4.yaxis.axis_label = 'Valores'

#un par de widgets
estilo = {'color':'white', 'font':'15px bold arial, sans-serif', 'background-color': 'green', 'text-align':'center', 'border-radius':'7px'}
U1_Text = PreText(text= 'u1: 0.00', width=300, style=estilo)

#inputs
v1_text = TextInput(value="0",title='Voltaje 1', default_size=100)
v2_text = TextInput(value="0",title='Voltaje 2', default_size=100)
r1_text = TextInput(value="0",title='Razón Flujo 1', default_size=100)
r2_text = TextInput(value="0",title='Razon Flujo 2', default_size=100)
h1_text = TextInput(value="0",title='Altura 1', default_size=100)
h2_text = TextInput(value="0",title='Altura 2', default_size=100)
kp_text = TextInput(value="0",title="Kp", default_size=66)
ki_text = TextInput(value="0",title="Ki", default_size=66)
kd_text = TextInput(value="0",title="Kd", default_size=66)
kp_text = TextInput(value="0",title="Kp", default_size=66)
compi_text = TextInput(value="0",title="Comp i", default_size=66)
compd_text = TextInput(value="0",title="Comp d", default_size=66)

#select format
output_format = Select(title="Formato:", value="csv", options=["csv", "npy", "txt"], default_size=100)

#radio botton group
mode = RadioButtonGroup(labels=["Automatico","Manual"], active=0, default_size=100)
mode.on_change('active', lambda attr, old, new: Mode(mode.active))
save = RadioButtonGroup(labels=["Stop", "Grabar"], active=0, default_size=100)
save.on_change('active', lambda attr, old, new: Save(save.active, output_format.value, data_saved))

#alerta
alert = Button(label = 'Normal', default_size=100, button_type='success')

def change_alert():
	global alert
	if (alert.label == 'Normal'):
		alert.label = 'Peligro'
		alert.button_type='danger'
	else:
		alert.label = 'Normal'
		alert.button_type = 'success'

t=0
def MainLoop():
	global lectura, t, data_saved, inputs
	update = dict(time=[t], 
		nu1=[lectura['nu1']], 
		nu2=[lectura['nu2']], 
		t1=[lectura['t1']], 
		t2=[lectura['t2']],
		t3=[lectura['t3']],
		t4=[lectura['t4']],
		h1=[float(h1_text.value)],
		h2=[float(h2_text.value)]
		)
	data.stream(new_data=update, rollover=100)#ultimos 100 datos
	if(save.active == 1):
		Saving(data_saved, mode.active)
	t += 1



l = layout([
	[fig_u1, [mode, save,[[v1_text, r1_text], [v2_text, r2_text]]],output_format],
	[fig_u2, h1_text, h2_text],
	[fig_t1, kp_text, ki_text, kd_text],
	[fig_t2, compi_text, compd_text, alert],
	[fig_t3],
	[fig_t4]
	])

print("----------------------------")
Mode(mode.active)
doc = curdoc()
doc.add_root(l)
doc.title = 'Dashboard' 
#doc.add_periodic_callback(GetValues, 200)
doc.add_periodic_callback(MainLoop, 300)# Cada 300mili se llama funcion y se actualiza grafico
