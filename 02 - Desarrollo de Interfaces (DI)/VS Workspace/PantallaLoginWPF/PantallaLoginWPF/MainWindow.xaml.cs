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

namespace PantallaLoginWPF
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

        /** Abre la ventana de registro (y cierra la actual) */
        private void Abrir_Registro(object sender, RoutedEventArgs e) { 
            Register ventanaRegistro = new Register();
            // Cierra la ventana principal
            this.Close();
            // Abre la ventana de registro
            ventanaRegistro.Show();
        }
        
        /** Abre la ventana de login (y cierra la actual) */
        private void Abrir_Login(object sender, RoutedEventArgs e) { 
            Login ventanaLogin = new Login();
            // Cierra la ventana principal
            this.Close();
            // Abre la ventana de registro
            ventanaLogin.Show();
        }

    }
}
