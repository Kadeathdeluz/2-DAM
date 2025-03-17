
using System.Text;
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
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class AñadidoEstudiantes : Window
    {
        private MainViewModel _viewModel;

        public AñadidoEstudiantes()
        {
            InitializeComponent();
            _viewModel = new MainViewModel();
        }
        
        // Creamos un nuevo Estudiante.
        private void btnAñadir_Click(object sender, RoutedEventArgs e)
        {
            // Declaramos variables necesarias para crear el nuevo Curso.
            string stNombre = txtNombre.Text;
            string stApellido = txtApellido.Text;
            string stEdad = txtEdad.Text;

            // Verificamos que estén todos los campos rellenos antes de crear el nuevo Estudiante y que en el campo Edad se guarde una variable int correcta.
            if (string.IsNullOrEmpty(stNombre) || string.IsNullOrEmpty(stApellido))
            {
                MessageBox.Show("Rellene todos los campos.", "Error creación Estudiante", MessageBoxButton.OK, MessageBoxImage.Warning);
            }
            else if (int.TryParse(txtEdad.Text, out int intEdad))
            {
                // Creamos el nuevo estudiante y lo añadimos al resto de estudiantes.
                var nuevoEstudiante = new Estudiante { Nombre = stNombre, Apellido = stApellido, Edad = intEdad };
                List<Estudiante> estudiantes = _viewModel.LeerXMLEstudiantes();
                estudiantes.Add(nuevoEstudiante);
                _viewModel.EscribirXMLEstudiantes(estudiantes);

                // Volvemos a la portada de la aplicación y cerramos esta.
                PaginaPrincipal paginaPrincipalWindow = new PaginaPrincipal();
                paginaPrincipalWindow.Show();
                Close();
            }
            else
            {
                MessageBox.Show("La edad ha de ser válida.", "Error creación Estudiante", MessageBoxButton.OK, MessageBoxImage.Warning);
            }

        }

        // Volvemos a la portada de la aplicación.
        private void btnVolver_Click(object sender, RoutedEventArgs e)
        {
            PaginaPrincipal paginaPrincipalWindow = new PaginaPrincipal();
            paginaPrincipalWindow.Show();
            Close();
        }
    }
}