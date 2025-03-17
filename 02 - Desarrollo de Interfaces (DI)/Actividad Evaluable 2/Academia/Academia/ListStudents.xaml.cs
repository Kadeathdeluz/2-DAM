using Academia.Data;
using Academia.ViewModel;
using System.Collections.ObjectModel;
using System.Windows.Controls;

namespace Academia
{
    /// <summary>
    /// Lógica de interacción para ListStudents.xaml
    /// </summary>
    public partial class ListStudents : Page
    {
        private AcademiaViewModel _viewModel;
        private ObservableCollection<Student> Students;
        
        public ListStudents(AcademiaViewModel viewModel)
        {
            InitializeComponent();

            _viewModel = viewModel;
            DataContext = _viewModel;

            //InitializeStudents();
            Students = _viewModel.Students;

            showStudentsDG.ItemsSource = Students;
        }
    }
}
