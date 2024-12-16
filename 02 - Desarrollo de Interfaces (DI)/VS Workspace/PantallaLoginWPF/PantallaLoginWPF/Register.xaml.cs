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
    /// Lógica de interacción para Register.xaml
    /// </summary>
    public partial class Register : Window
    {
        public Register()
        {
            InitializeComponent();
        }

        /** Abre una nueva ventana de inicio (y cierra la actual de Registro) */
        private void Abrir_Inicio(object sender, RoutedEventArgs e)
        {
            MainWindow ventanaInicio = new MainWindow();
            this.Close();
            ventanaInicio.Show();
        }

        private void BotonRegistro_Click(object sender, RoutedEventArgs e)
        {
            String mensaje = "";

            mensaje += "Usuario: " + textboxUser.Text
                + "\nContraseña: " + textboxContrasenya.Password
                + "\n creado correctamente.";

            textboxUser.Text = "";
            textboxContrasenya.Password = "";

            MessageBox.Show(mensaje);
        }
    }
}
