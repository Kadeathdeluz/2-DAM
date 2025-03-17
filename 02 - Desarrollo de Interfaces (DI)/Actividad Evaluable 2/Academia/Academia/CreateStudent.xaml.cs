using Academia.Data;
using Academia.ViewModel;
using System.Linq;
using System.Windows;
using System.Windows.Controls;

namespace Academia
{
    /// <summary>
    /// Lógica de interacción para CreateStudent.xaml
    /// </summary>
    public partial class CreateStudent : Page
    {
        private AcademiaViewModel _viewModel;

        public CreateStudent(AcademiaViewModel viewModel)
        {
            InitializeComponent();

            _viewModel = viewModel;
            DataContext = _viewModel;
        }

        // Al hacer click en el botón aceptar, se agrega un nuevo curso a la lista de cursos
        private void AcceptButton_Click(object sender, RoutedEventArgs e)
        {
            if (ageTextBox.Text.All(char.IsDigit) == false)
            {
                MessageBox.Show("Introduzca una edad correcta.");
                return;
            }
            if (firstNameTextBox.Text == "" || lastNameTextBox.Text == "" || ageTextBox.Text == "")
            {
                MessageBox.Show("Por favor, llene todos los campos.");
                return;
            }
            _viewModel.Students.Add(new Student
            (
                firstNameTextBox.Text,
                lastNameTextBox.Text,
                int.Parse(ageTextBox.Text)
            ));

            MessageBox.Show("Estudiante agregado exitosamente.");
            clearFields();

        }

        // Método para limpiar los campos de texto al hacer click en el botón cancelar
        private void CancelButton_Click(object sender, RoutedEventArgs e)
        {
            clearFields();
        }

        // Método auxiliar para limpiar los campos de texto
        private void clearFields() {
            firstNameTextBox.Text = "";
            lastNameTextBox.Text = "";
            ageTextBox.Text = "";
        }
    }
}
