import subprocess
import streamlit as st

def list_installed_packages(show_core_packages=True):
    result = subprocess.run(['pip', 'list'], stdout=subprocess.PIPE, text=True)
    installed_packages = result.stdout.split('\n')[2:]
    packages = [package.split()[0] for package in installed_packages if package]

    if not show_core_packages:
        # Filter out core packages
        core_packages = ['python', 'pip', 'setuptools']
        packages = [package for package in packages if package.lower() not in core_packages]

    return packages

def get_package_info(package_name):
    result = subprocess.run(['pip', 'show', package_name], stdout=subprocess.PIPE, text=True)
    return result.stdout

def remove_package(package_name):
    subprocess.run(['pip', 'uninstall', package_name])

def is_core_package(package_name):
    # Add names of core packages that are critical for Python
    core_packages = ['python', 'pip', 'setuptools']
    return package_name.lower() in core_packages

def main():
    st.set_page_config(page_title="Python Package Uninstaller", page_icon=":files:")
    st.title('Python Package Uninstaller')
    st.text('Created with ChatGPT')
    show_core_packages = st.checkbox('Show Core Packages')
    installed_packages = list_installed_packages(show_core_packages)

    st.header('Installed Packages')
    selected_package = st.selectbox('Select a package to remove:', installed_packages)

    if st.button('Remove Selected Package'):
        if selected_package:
            if show_core_packages or not is_core_package(selected_package):
                package_info = get_package_info(selected_package)
                st.text(f"Package Information for {selected_package}:\n{package_info}")
                confirm = st.radio("Do you want to remove this package?", ('Yes', 'No'))
                if confirm == 'Yes':
                    remove_package(selected_package)
                    st.success(f'{selected_package} has been removed.')
                else:
                    st.warning(f'Removal of {selected_package} canceled.')

    st.text('You will need to confirm for removal on your terminal!')
    st.subheader('List of Installed Packages:')
    st.write(installed_packages)

if __name__ == '__main__':
    main()