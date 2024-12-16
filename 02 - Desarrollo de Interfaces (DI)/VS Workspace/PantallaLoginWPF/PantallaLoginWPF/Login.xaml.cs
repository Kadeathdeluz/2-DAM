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
using System.Windows.Shapes;

namespace PantallaLoginWPF
{
    /// <summary>
    /// Lógica de interacción para Login.xaml
    /// </summary>
    public partial class Login : Window
    {
        private const String USUARIO = "ElPrimo";
        private const String CONTRASENYA = "123456";
        public Login()
        {
            InitializeComponent();

        }

        /** Abre una nueva ventana de inicio (y cierra la actual de Login) */
        private void Abrir_Inicio(object sender, RoutedEventArgs e)
        {
            MainWindow ventanaInicio = new MainWindow();
            this.Close();
            ventanaInicio.Show();
        }

        private void BotonLogin_Click(object sender, RoutedEventArgs e)
        {
            if (textboxUser.Text == USUARIO && textboxContrasenya.Password == CONTRASENYA)
            {
                MessageBox.Show("Login realizado con éxito.");
            }
            else {
                MessageBox.Show("Usuario o contraseña incorrectos.");
            }
        }
    }
}
