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

namespace Academia
{
    /// <summary>
    /// Lógica de interacción para Home.xaml
    /// </summary>
    public partial class Home : Page
    {
        public Home()
        {
            InitializeComponent();
        }

        // Evento mouse enter para el texto de login: Cambia el color de fondo del botón
        private void loginTB_MouseEnter(object sender, MouseEventArgs e)
        {
            // Cambia el color de fondo del botón al entrar el mouse
            loginTB.Background = Brushes.Blue;
            loginTB.Foreground = Brushes.White;
        }

        // Evento mouse leave para el texto de login: Vuelve a su color original
        private void loginTB_MouseLeave(object sender, MouseEventArgs e)
        {
            // Cambia el color de fondo del botón al salir el mouse
            loginTB.Background = Brushes.White;
            loginTB.Foreground = Brushes.Black;

        }
        // Evento mouse enter para el texto de crear cuenta: Cambia el color de fondo del botón 
        private void createAccountTB_MouseEnter(object sender, MouseEventArgs e)
        {
            // Cambia el color de fondo del botón al entrar el mouse
            createAccountTB.Background = Brushes.Blue;
            createAccountTB.Foreground = Brushes.White;

        }

        // Evento mouse leave para el texto de crear cuenta: Vuelve a su color original
        private void createAccountTB_MouseLeave(object sender, MouseEventArgs e)
        {
            // Cambia el color de fondo del botón al salir el mouse
            createAccountTB.Background = Brushes.White;
            createAccountTB.Foreground = Brushes.Black;

        }

        private void loginTB_Click(object sender, RoutedEventArgs e)
        {
            MessageBox.Show("Futura implementación: Inicio de Sesión");
        }

        private void createAccountTB_Click(object sender, RoutedEventArgs e)
        {
            MessageBox.Show("Futura implementación: Crear cuenta");
        }
    }


}
