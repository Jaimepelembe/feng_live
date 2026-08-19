#Adicionar a Raiz ao sys.path (Executando Direto) Para que possa importar sem problemas
import sys
import os

# Adiciona a pasta raiz 'sga' ao path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from controller.estudanteController import EstudanteController
estudanteController=EstudanteController()

import PySimpleGUI as sg
class EstudanteGUI:
    
    def __init__(self):
        self.id_estudante=""    
        self.numero_estudante=""    
        self.nome=""
        self.email=""
        self.id_curso=""
        self.window=None
        self.running=True # The window is running?
        self.create_window()
    
    def create_window(self):
        """Cria a janela principal do aluno"""
        
        # Define o tema
        sg.theme('DarkBlue')
        
        # Layout de conexão
        connection_layout = [
            [sg.Text('📧 Email:', size=(14, 1)), 
             sg.InputText('', key='-EMAIL-', size=(30, 1))],
            [sg.Text('🎓 Nr. Estudante:', size=(14, 1)), 
             sg.InputText('', key='-NRESTUDANTE-', password_char='*', size=(20, 1))],
            [sg.Text('🌐 Servidor:', size=(14, 1)), 
             sg.InputText(estudanteController.SERVERADDRESS, key='-HOST-', size=(20, 1))],
            [sg.Text('🔌 Porta:', size=(14, 1)), 
             sg.InputText(str(estudanteController.PORT), key='-PORT-', size=(20, 1))],
            [sg.Button('🔗 Conectar', key='-CONNECT-', size=(15, 1), button_color=('white', '#27AE60')),
             sg.Button('🚪 Desconectar', key='-DISCONNECT-', size=(15, 1), button_color=('white', '#E74C3C'), disabled=True)],
        ]
        
        # Layout de status
        status_layout = [
            [sg.Text('Status:', size=(10, 1), text_color='white'),
             sg.Text('Desconectado', key='-STATUS-', size=(30, 1), text_color='#E74C3C')],
            [sg.Text('Aluno:', size=(10, 1), text_color='white'),
             sg.Text('', key='-NOME-', size=(30, 1), text_color='#3498DB')],
        ]
        
        # Layout de informações do aluno
        info_layout = [
            [sg.Frame('📊 Informações Acadêmicas', layout=[
                [sg.Text('Média Geral:', size=(15, 1), text_color='white'),
                 sg.Text('0.0', key='-MEDIA-', size=(10, 1), text_color='#F1C40F', font=('Arial', 14, 'bold'))],
                [sg.Text('Disciplinas:', size=(15, 1), text_color='white'),
                 sg.Text('0', key='-DISCIPLINAS-', size=(10, 1), text_color='#3498DB')],
                [sg.Text('Notificações:', size=(15, 1), text_color='white'),
                 sg.Text('0', key='-NOTIFICACOES-', size=(10, 1), text_color='#2ECC71')],
            ], background_color='#2C3E50', title_color='white')]
        ]
        
        # Layout do tabuleiro de notas
        notas_layout = [
            [sg.Frame('📚 Minhas Notas', layout=[
                [sg.Table(
                    values=[],
                    headings=['Disciplina', 'Nota 1', 'Nota 2', 'Nota 3', 'Média', 'Frequência', 'Semestre'],
                    key='-NOTAS_TABLE-',
                    auto_size_columns=False,
                    col_widths=[15, 8, 8, 8, 8, 10, 10],
                    num_rows=8,
                    header_background_color='#34495E',
                    header_text_color='white',
                    background_color='#2C3E50',
                    text_color='white',
                    alternating_row_color='#34495E',
                )]
            ], background_color='#2C3E50', title_color='white', size=(700, 200))]
        ]
        
        # Layout de ações
        actions_layout = [
            [sg.Button('🔄 Atualizar Notas', key='-UPDATE-', size=(15, 1), button_color=('white', '#3498DB')),
             sg.Button('📊 Ver Média', key='-MEDIA_BTN-', size=(15, 1), button_color=('white', '#1ABC9C')),
             sg.Button('📨 Ver Notificações', key='-NOTIFICACOES_BTN-', size=(15, 1), button_color=('white', '#F39C12')),
             sg.Button('💬 Chat', key='-CHAT-', size=(15, 1), button_color=('white', '#9B59B6'))],
        ]
        
        # Layout de chat/broadcast
        chat_layout = [
            [sg.Frame('💬 Chat - Broadcast', layout=[
                [sg.Multiline('', key='-CHAT_DISPLAY-', size=(80, 8), 
                             disabled=True, background_color='#34495E', 
                             text_color='white', font=('Consolas', 10))],
                [sg.InputText('', key='-CHAT_INPUT-', size=(60, 1), 
                             background_color='#ECF0F1', text_color='#2C3E50'),
                 sg.Button('📤 Enviar', key='-CHAT_SEND-', size=(10, 1), 
                          button_color=('white', '#3498DB'))]
            ], background_color='#2C3E50', title_color='white')]
        ]
        
        # Layout da janela
        layout = [
            [sg.Column(connection_layout, background_color='#2C3E50')],
            [sg.HSeparator()],
            [sg.Column(status_layout, background_color='#2C3E50')],
            [sg.Column(info_layout, background_color='#2C3E50')],
            [sg.Column(notas_layout, background_color='#2C3E50')],
            [sg.Column(actions_layout, background_color='#2C3E50')],
            [sg.Column(chat_layout, background_color='#2C3E50')],
        ]
        
        # Cria a janela
        self.window = sg.Window(
            '🎓 FENG-LIVE - Aluno',
            layout,
            size=(800, 750),
            background_color='#2C3E50',
            finalize=True,
            resizable=True
        )
        
        
    def autenticarEstudante(self, values):
        """Conecta ao servidor"""
        email = values['-EMAIL-'].strip()
        nrEstudante = values['-NRESTUDANTE-'].strip()
        
        if not email or not nrEstudante:
            sg.popup_error('Preencha o email e o numero de estudante!')
            return
        
        try:
            estudanteController.start()
            dados=estudanteController.autenticarEstudande(email,nrEstudante)
            print(f"GUI: {dados}")
            
            if dados:
                dados=dados["valor"]
                self.id_estudante=dados["id"]
                self.numero_estudante=dados["numero_estudante"]
                self.nome=dados["nome"]
                self.email=dados["email"]
                self.id_curso=dados["id_curso"]

                
                # Atualiza status
                self.window['-STATUS-'].update('Conectado', text_color='#2ECC71')
                self.window['-NOME-'].update(self.nome)
                self.window['-CONNECT-'].update(disabled=True)
                self.window['-DISCONNECT-'].update(disabled=False)
                
                # Busca dados iniciais
                #self.update_notas()
                #self.update_media()
                
                
                sg.popup_ok('✅ Conectado com sucesso!')
         
    
            

            
            # Notificações/broadcasts chegam via callback da thread de leitura do BaseClient
            #self.client.on_push = self.handle_push
            #self.client.on_disconnect = self.handle_disconnect


                
            
            #else:
            #    sg.popup_error('❌ Falha na conexão. Verifique suas credenciais.')
                
        except Exception as e:
            sg.popup_error(f'❌ Erro ao conectar: {e}') 
   
   
   
    
    def run(self):
        """Loop principal da GUI"""
        while self.running:
            event, values = self.window.read(timeout=100)
            
            if event == sg.WIN_CLOSED:
                self.running = False
                #if self.connected:
                #    pass
                   #  self.disconnect()
                break
            
            if event == '-CONNECT-':
                self.autenticarEstudante(values)
                pass
                #self.connect(values)
            
            elif event == '-DISCONNECT-':
                pass
                #self.disconnect()
            
            elif event == '-UPDATE-':
                pass
                #self.update_notas()
                #self.update_media()
            
            elif event == '-MEDIA_BTN-':
                #self.update_media()
                sg.popup(f'📊 Média Geral: {self.media:.1f}' if self.media else '📊 Sem dados de média',
                         title='Média Geral')
            
            elif event == '-NOTIFICACOES_BTN-':
                self.show_notificacoes()
            
            elif event == '-CHAT_SEND-':
                pass
                #message = values['-CHAT_INPUT-'].strip()
                #self.send_broadcast(message)
            
            elif event == '-CHAT-':
                pass
                #sg.popup('💬 Chat em tempo real!\n\nEnvie mensagens usando BROADCAST\n\nDica: Todos os conectados verão sua mensagem.',#     title='Chat')
        
        self.window.close()
        
Gui=EstudanteGUI()
Gui.run()