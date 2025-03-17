using Academia.Data;
using Academia.ViewModel;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
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
    /// Lógica de interacción para CreateCourse.xaml
    /// </summary>
    public partial class CreateCourse : Page
    {
        private AcademiaViewModel _viewModel;

        public CreateCourse(AcademiaViewModel viewModel)
        {
            InitializeComponent();

            // Inicializamos el ViewModel
            _viewModel = viewModel;
            DataContext = _viewModel;
        }

        // Al hacer click en el botón aceptar, se agrega un nuevo curso a la lista de cursos
        private void AcceptButton_Click(object sender, RoutedEventArgs e)
        {
            if (durationTextBox.Text.All(char.IsDigit) == false)
            {
                MessageBox.Show("Introduzca una duración correcta.");
                return;
            }
            if (courseNameTextBox.Text == "" || durationTextBox.Text == "" || professorNameTextBox.Text == "")
            {
                MessageBox.Show("Por favor, llene todos los campos.");
                return;
            }
            _viewModel.Courses.Add(new Course
            (
                courseNameTextBox.Text,
                int.Parse(durationTextBox.Text),
                professorNameTextBox.Text
            ));

            MessageBox.Show("Curso agregado exitosamente.");
            clearFields();
        }

        // Método para limpiar los campos de texto al hacer click en el botón cancelar
        private void CancelButton_Click(object sender, RoutedEventArgs e)
        {
            clearFields();
        }

        // Método auxiliar para limpiar los campos de texto
        private void clearFields()
        {
            courseNameTextBox.Text = "";
            durationTextBox.Text = "";
            professorNameTextBox.Text = "";
        }


    }
}
