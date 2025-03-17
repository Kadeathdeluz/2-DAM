using System;
using System.Collections.Generic;
using System.ComponentModel;
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

namespace AcademiaSergioAdellJorge
{
    /// <summary>
    /// Lógica de interacción para UserControl1.xaml
    /// </summary>
    public partial class UserControlTxtBox : UserControl
    {
        public UserControlTxtBox()
        {
            DataContext = this;
            InitializeComponent();
        }

        // Evento que dispara cuando una propiedad cambia.
        public event PropertyChangedEventHandler? PropertyChanged;

        // Propiedad NombreValor.
        private string nombrevalor;
        public string NombreValor
        {
            get { return nombrevalor; }
            set
            {
                nombrevalor = value;
                tbNombreValor.Text = nombrevalor;
                OnPropertyChanged(nameof(NombreValor));
            }
        }

        // Propiedad Valor.
        private string valor;

        public string Valor
        {
            get { return valor; }
            set
            {
                valor = value;
                txtValor.Text = valor;
                OnPropertyChanged(nameof(Valor));
            }
        }

        // Propiedad Text: obtiene o establece el texto del TextBox, para luego recogerlo para su tratamiento.
        public string Text
        {
            get
            {
                return txtValor.Text;
            }
            set
            {
            }
        }

        // Borramos el texto que haya en ese momento en el TextBox.
        private void btnBorrar_Click(object sender, RoutedEventArgs e)
        {
            // limpiamos el contenido del TextBox.
            txtValor.Clear();
            // ponemos el foco en el TextBox.
            txtValor.Focus();
        }


        private void OnPropertyChanged(string propertyName)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }
    }
}
