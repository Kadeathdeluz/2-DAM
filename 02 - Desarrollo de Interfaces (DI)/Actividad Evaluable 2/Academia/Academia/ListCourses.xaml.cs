using Academia.Data;
using Academia.ViewModel;
using System.Collections.ObjectModel;
using System.Windows;
using System.Windows.Controls;

namespace Academia
{
    /// <summary>
    /// Lógica de interacción para ListCourses.xaml
    /// </summary>
    public partial class ListCourses : Page
    {
        private AcademiaViewModel _viewModel;
        private ObservableCollection<Course> Courses;


        public ListCourses(AcademiaViewModel viewModel)
        {
            InitializeComponent();

            _viewModel = viewModel;
            DataContext = _viewModel;

            //InitializeCouses();
            Courses = _viewModel.Courses;

            showCoursesDG.ItemsSource = Courses;
        }

    }
}
