from metacli import dependency_management

dm = dependency_management.DependencyManagement()

dm.gather_packages_for_plugins_and_check_conflicts()
