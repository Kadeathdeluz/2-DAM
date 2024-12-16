using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace Pre_Examen
{
    /// <summary>
    /// Lógica de interacción para MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
        }

        /** Al hacer click en acerca de en el menú contextual, se abre una ventana con el texto y título especificados */
        private void AcercaDe_Click(object sender, RoutedEventArgs e) {
            MessageBox.Show("Esta aplicación ha sido desarrollada por Roldán Sanchis Martínez", "Acerca de");
        }

        /** Al hacer click en Seleccionar todo en el menú contextual, no hace nada */
        private void SeleccionarTodo_Click(object sender, RoutedEventArgs e) {
            // No hace nada, pero es checkeable mediante interfaz
        }
    }
}
