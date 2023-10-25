import sys
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QLabel, QWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton,QGroupBox
from PyQt5.QtGui import QDoubleValidator
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from mpl_toolkits.mplot3d import Axes3D, art3d
from Config import *
import numpy as np
from cam import Camera 
from obj import Object


###### Crie suas funções de translação, rotação, criação de referenciais, plotagem de setas e qualquer outra função que precisar

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.cam = Camera()
        self.obj = Object()
        #definindo as variaveis
        self.set_variables()
        #Ajustando a tela    
        self.setWindowTitle("Grid Layout")
        self.setGeometry(100, 100,1280 , 720)
        self.setup_ui()
        self.x_lim = 1280
        self.y_lim = 720

    def set_variables(self):
        self.objeto_original = [] #modificar
        self.objeto = self.objeto_original
        self.cam_original = [] #modificar
        self.px_base = 1280  #modificar
        self.px_altura = 720 #modificar
        self.dist_foc = 1 #modificar
        self.stheta = 0 #modificar
        self.ox = self.px_base/2 #modificar
        self.oy = self.px_altura/2 #modificar
        self.ccd = [4,3] #modificar
        self.projection_matrix = [] #modificar
        
    def setup_ui(self):
        # Criar o layout de grade
        grid_layout = QGridLayout()

        # Criar os widgets
        line_edit_widget1 = self.create_world_widget("Ref mundo")
        line_edit_widget2  = self.create_cam_widget("Ref camera")
        line_edit_widget3  = self.create_intrinsic_widget("params instr")

        self.canvas = self.create_matplotlib_canvas()

        # Adicionar os widgets ao layout de grade
        grid_layout.addWidget(line_edit_widget1, 0, 0)
        grid_layout.addWidget(line_edit_widget2, 0, 1)
        grid_layout.addWidget(line_edit_widget3, 0, 2)
        grid_layout.addWidget(self.canvas, 1, 0, 1, 3)

          # Criar um widget para agrupar o botão de reset
        reset_widget = QWidget()
        reset_layout = QHBoxLayout()
        reset_widget.setLayout(reset_layout)

        # Criar o botão de reset vermelho
        reset_button = QPushButton("Reset")
        reset_button.setFixedSize(50, 30)  # Define um tamanho fixo para o botão (largura: 50 pixels, altura: 30 pixels)
        style_sheet = """
            QPushButton {
                color : white ;
                background: rgba(255, 127, 130,128);
                font: inherit;
                border-radius: 5px;
                line-height: 1;
            }
        """
        reset_button.setStyleSheet(style_sheet)
        reset_button.clicked.connect(self.reset_canvas)

        # Adicionar o botão de reset ao layout
        reset_layout.addWidget(reset_button)

        # Adicionar o widget de reset ao layout de grade
        grid_layout.addWidget(reset_widget, 2, 0, 1, 3)

        # Criar um widget central e definir o layout de grade como seu layout
        central_widget = QWidget()
        central_widget.setLayout(grid_layout)
        
        # Definir o widget central na janela principal
        self.setCentralWidget(central_widget)

    def create_intrinsic_widget(self, title):
        # Criar um widget para agrupar os QLineEdit
        line_edit_widget = QGroupBox(title)
        line_edit_layout = QVBoxLayout()
        line_edit_widget.setLayout(line_edit_layout)

        # Criar um layout de grade para dividir os QLineEdit em 3 colunas
        grid_layout = QGridLayout()

        line_edits = []
        labels = ['n_pixels_base:', 'n_pixels_altura:', 'ccd_x:', 'ccd_y:', 'dist_focal:', 'sθ:']  # Texto a ser exibido antes de cada QLineEdit

        # Adicionar widgets QLineEdit com caixa de texto ao layout de grade
        for i in range(1, 7):
            line_edit = QLineEdit()
            label = QLabel(labels[i-1])
            validator = QDoubleValidator()  # Validador numérico
            line_edit.setValidator(validator)  # Aplicar o validador ao QLineEdit
            grid_layout.addWidget(label, (i-1)//2, 2*((i-1)%2))
            grid_layout.addWidget(line_edit, (i-1)//2, 2*((i-1)%2) + 1)
            line_edits.append(line_edit)

        # Criar o botão de atualização
        update_button = QPushButton("Atualizar")

        ##### Você deverá criar, no espaço reservado ao final, a função self.update_params_intrinsc ou outra que você queira 
        # Conectar a função de atualização aos sinais de clique do botão
        update_button.clicked.connect(lambda: self.update_params_intrinsc(line_edits))

        # Adicionar os widgets ao layout do widget line_edit_widget
        line_edit_layout.addLayout(grid_layout)
        line_edit_layout.addWidget(update_button)

        # Retornar o widget e a lista de caixas de texto
        return line_edit_widget
    
    def create_world_widget(self, title):
        # Criar um widget para agrupar os QLineEdit
        line_edit_widget = QGroupBox(title)
        line_edit_layout = QVBoxLayout()
        line_edit_widget.setLayout(line_edit_layout)

        # Criar um layout de grade para dividir os QLineEdit em 3 colunas
        grid_layout = QGridLayout()

        line_edits = []
        labels = ['X(move):', 'X(angle):', 'Y(move):', 'Y(angle):', 'Z(move):', 'Z(angle):']  # Texto a ser exibido antes de cada QLineEdit

        # Adicionar widgets QLineEdit com caixa de texto ao layout de grade
        for i in range(1, 7):
            line_edit = QLineEdit()
            label = QLabel(labels[i-1])
            validator = QDoubleValidator()  # Validador numérico
            line_edit.setValidator(validator)  # Aplicar o validador ao QLineEdit
            grid_layout.addWidget(label, (i-1)//2, 2*((i-1)%2))
            grid_layout.addWidget(line_edit, (i-1)//2, 2*((i-1)%2) + 1)
            line_edits.append(line_edit)

        # Criar o botão de atualização
        update_button = QPushButton("Atualizar")
        ##### Você deverá criar, no espaço reservado ao final, a função self.update_world ou outra que você queira 
        # Conectar a função de atualização aos sinais de clique do botão
        update_button.clicked.connect(lambda: self.update_world(line_edits))

        # Adicionar os widgets ao layout do widget line_edit_widget
        line_edit_layout.addLayout(grid_layout)
        line_edit_layout.addWidget(update_button)
        # Retornar o widget e a lista de caixas de texto
        return line_edit_widget
    
    def create_cam_widget(self, title):
        # Criar um widget para agrupar os QLineEdit
        line_edit_widget = QGroupBox(title)
        line_edit_layout = QVBoxLayout()
        line_edit_widget.setLayout(line_edit_layout)

        # Criar um layout de grade para dividir os QLineEdit em 3 colunas
        grid_layout = QGridLayout()

        line_edits = []
        labels = ['X(move):', 'X(angle):', 'Y(move):', 'Y(angle):', 'Z(move):', 'Z(angle):']  # Texto a ser exibido antes de cada QLineEdit

        # Adicionar widgets QLineEdit com caixa de texto ao layout de grade
        for i in range(1, 7):
            line_edit = QLineEdit()
            label = QLabel(labels[i-1])
            validator = QDoubleValidator()  # Validador numérico
            line_edit.setValidator(validator)  # Aplicar o validador ao QLineEdit
            grid_layout.addWidget(label, (i-1)//2, 2*((i-1)%2))
            grid_layout.addWidget(line_edit, (i-1)//2, 2*((i-1)%2) + 1)
            line_edits.append(line_edit)

        # Criar o botão de atualização
        update_button = QPushButton("Atualizar")

        ##### Você deverá criar, no espaço reservado ao final, a função self.update_cam ou outra que você queira 
        # Conectar a função de atualização aos sinais de clique do botão
        update_button.clicked.connect(lambda: self.update_cam(line_edits))

        # Adicionar os widgets ao layout do widget line_edit_widget
        line_edit_layout.addLayout(grid_layout)
        line_edit_layout.addWidget(update_button)

        # Retornar o widget e a lista de caixas de texto
        return line_edit_widget

    def create_matplotlib_canvas(self):
        # Criar um widget para exibir os gráficos do Matplotlib
        canvas_widget = QWidget()
        canvas_layout = QHBoxLayout()
        canvas_widget.setLayout(canvas_layout)

        # Criar um objeto FigureCanvas para exibir o gráfico 2D
        self.fig1, self.ax1 = plt.subplots()
        self.ax1.set_title("Imagem")
        self.canvas1 = FigureCanvas(self.fig1)

        ##### Falta acertar os limites do eixo X
        self.ax1.set_xlim([0,1280])
        ##### Falta acertar os limites do eixo Y
        self.ax1.set_ylim([720,0])


        self.fig2 = plt.figure()
        self.ax2 = self.fig2.add_subplot(111, projection='3d')

        plt.ion()

        
        # Criar um objeto FigureCanvas para exibir o gráfico 3D
        self.stl_plot = self.obj.STL()
        self.stl_vectors = self.obj.STL_vetor() 
        self.ax2.add_collection3d(art3d.Poly3DCollection(self.stl_vectors))
        self.ax2.add_collection3d(art3d.Line3DCollection(self.stl_vectors, colors='k', linewidths=0.2, linestyles='-'))
        self.ax2.auto_scale_xyz(self.stl_plot[0,:],self.stl_plot[1,:],self.stl_plot[2,:])
        self.set_axes_equal(self.ax2)
        self.ax2.view_init(elev=45,azim=-35)
        self.ax2.dist=10

        ##### Você deverá criar a função de projeção 
        self.world_refx, self.world_refy, self.world_refz = self.draw_arrows(POINT,BASE,self.ax2,15)
        self.cam_refx, self.cam_refy, self.cam_refz = self.draw_arrows(self.cam.M[:,3],self.cam.M[:,0:3],self.ax2, 10)
        object_2d = self.projection_2d()

        ##### Falta plotar o object_2d que retornou da projeção
        self.obj_view = self.ax1.plot(object_2d[0, :], object_2d[1, :], color = (0.2, 0.2, 0.2, 0.9), linewidth = 0.3) 

        self.ax1.grid('True')
        self.ax1.set_aspect('equal')  
        canvas_layout.addWidget(self.canvas1)
    
        
        ##### Falta plotar o seu objeto 3D e os referenciais da câmera e do mundo
        object_2d = self.projection_2d()

        self.canvas2 = FigureCanvas(self.fig2)
        canvas_layout.addWidget(self.canvas2)

        # Retornar o widget de canvas
        return canvas_widget


    ##### Você deverá criar as suas funções aqui
    def set_axes_equal(self, ax):

        x_limits = ax.get_xlim3d()
        y_limits = ax.get_ylim3d()
        z_limits = ax.get_zlim3d()

        x_range = abs(x_limits[1] - x_limits[0])
        x_middle = np.mean(x_limits)
        y_range = abs(y_limits[1] - y_limits[0])
        y_middle = np.mean(y_limits)
        z_range = abs(z_limits[1] - z_limits[0])
        z_middle = np.mean(z_limits)

    
        plot_radius = 0.5*max([x_range, y_range, z_range])

        ax.set_xlim3d([x_middle - plot_radius, x_middle + plot_radius])
        ax.set_ylim3d([y_middle - plot_radius, y_middle + plot_radius])
        ax.set_zlim3d([z_middle - plot_radius, z_middle + plot_radius])
    
    def draw_arrows(self, point,base,axis,length):
    # Plot vector of x-axis
        x = axis.quiver(point[0],point[1],point[2],base[0,0],base[1,0],base[2,0],color='red',pivot='tail',  length=length)
        # Plot vector of y-axis
        y = axis.quiver(point[0],point[1],point[2],base[0,1],base[1,1],base[2,1],color='green',pivot='tail',  length=length)
        # Plot vector of z-axis
        z = axis.quiver(point[0],point[1],point[2],base[0,2],base[1,2],base[2,2],color='blue',pivot='tail',  length=length)

        return x,y,z


    def update_params_intrinsc(self, line_edits):
        new_update = []

        for i in range(len(line_edits)):
            if line_edits[i].text() == '':
                new_update.append(0)
            else:
                new_update.append(float(line_edits[i].text()))

        self.cam.update_intrinsix_matrix(new_update)
        self.update_canvas(new_update[0],new_update[1])

    def update_world(self,line_edits):
        new_update = []

        for i in range(len(line_edits)):
            if line_edits[i].text() == '':
                new_update.append(0)
            else:
                new_update.append(float(line_edits[i].text()))

        self.T = self.cam.generate_move_world(new_update[0],new_update[2],new_update[4])
        self.cam.move_world()
        self.rotation = self.cam.generate_rotation_world(new_update[1],new_update[3],new_update[5])
        self.cam.rotation_world()
        self.cam_refx.remove()
        self.cam_refy.remove()
        self.cam_refz.remove()
        self.cam_refx, self.cam_refy, self.cam_refz = self.draw_arrows(self.cam.M[:,3],self.cam.M[:,0:3],self.ax2, 10)
        self.g = self.cam.generate_extrinsix_matrix()
        self.update_canvas(self.x_lim,self.y_lim)

    def update_cam(self,line_edits):
        new_update = []
        for i in range(len(line_edits)):
            if line_edits[i].text() == '':
                new_update.append(0)
            else:
                new_update.append(float(line_edits[i].text()))

        self.cam.move_cam(new_update[0],new_update[2],new_update[4])
        self.cam.rotation_cam(new_update[1],new_update[3],new_update[5])
        self.cam_refx.remove()
        self.cam_refy.remove()
        self.cam_refz.remove()
        self.cam_refx, self.cam_refy, self.cam_refz = self.draw_arrows(self.cam.M[:,3],self.cam.M[:,0:3],self.ax2, 10)
        self.g = self.cam.generate_extrinsix_matrix()
        self.update_canvas(self.x_lim,self.y_lim)

    def projection_2d(self):
       pi_zero = np.array([[1,0,0,0],
                           [0,1,0,0],
                           [0,0,1,0]])
       int_mat = self.cam.generate_intrinsix_matrix()
       ext_mat = self.cam.generate_extrinsix_matrix()
       self.projection = int_mat@pi_zero@np.linalg.inv(ext_mat)@self.stl_plot

       self.projection[0,:] = self.projection[0,:] / self.projection[2,:]
       self.projection[1,:] = self.projection[1,:] / self.projection[2,:]
       
       print("int mat")
       print(int_mat)
       print("ext mat")
       print(ext_mat)
       print("stl_plot")
       print(self.stl_plot)
       print("self.projection")
       print(self.projection)

       return self.projection 


    def update_canvas(self, x_lim, y_lim):
        for item in self.obj_view:
            item.remove()
            
        object_2d = self.projection_2d()
        self.obj_view = self.ax1.plot(object_2d[0, :], object_2d[1, :], color = (0.2, 0.2, 0.2, 0.9), linewidth = 0.3)
        
        self.x_lim = x_lim
        self.y_lim = y_lim
        self.ax1.set_xlim([0,self.x_lim])
        self.ax1.xaxis.tick_top()
        self.ax1.set_ylim([self.y_lim,0])

    def reset_canvas(self):
        return
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())