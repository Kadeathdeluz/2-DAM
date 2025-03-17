using System;
using System.ComponentModel;
using System.Printing;
using System.Windows.Controls;


namespace EjercicioTema5
{
    public partial class UserControl1 : UserControl, INotifyPropertyChanged
    {
        public UserControl1()
        {
            InitializeComponent();
            DataContext = this;
        }

        private string etiqueta;
        public string Etiqueta
        {
            get { return etiqueta; }
            set
            {
                etiqueta = value;
                OnPropertyChanged(nameof(Etiqueta));
            }
        }

        private string alturaCelda;
        public string AlturaCelda
        {
            get { return alturaCelda; }
            set
            {
                alturaCelda = value;
                OnPropertyChanged(nameof(AlturaCelda));
            }
        }

        private int caracteresMaximo;
        public int CaracteresMaximo
        {
            get { return caracteresMaximo; }
            set
            {
                caracteresMaximo = value;
                OnPropertyChanged(nameof(CaracteresMaximo));
                UpdateCharCounter();
            }
        }

        private string texto;
        public string Texto
        {
            get { return texto; }
            set
            {
                texto = value;
                OnPropertyChanged(nameof(Texto));
                UpdateCharCounter();
            }
        }

        public string Contador => $"{Texto?.Length ?? 0}/{CaracteresMaximo}";

        private void UpdateCharCounter()
        {
            OnPropertyChanged(nameof(Contador));
        }

        private void InputBox_TextChanged(object sender, TextChangedEventArgs e)
        {
            if (txtTexto.Text.Length > CaracteresMaximo)
            {
                txtTexto.Text = txtTexto.Text.Substring(0, CaracteresMaximo);
                txtTexto.CaretIndex = CaracteresMaximo;
            }
            Texto = txtTexto.Text;
        }

        public event PropertyChangedEventHandler PropertyChanged;

        private void OnPropertyChanged(string propertyName)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }
    }
}
