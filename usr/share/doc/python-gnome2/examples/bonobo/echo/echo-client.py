import bonobo
import Bonobo

bonobo.activate ()

obj = bonobo.get_object ('OAFIID:Bonobo_Sample_Echo', 'Bonobo/Sample/Echo')
obj.echo ('This is the message from the python client\n')

