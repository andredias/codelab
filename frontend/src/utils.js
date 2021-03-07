const languages = {
    py: 'Python',
}


export function filepath_to_language(filepath) {
    let filename = filepath.split('/').slice(-1)[0]
    let parts = filename.split('.')
    if (parts.lenght < 2) {
        return ''
    }
    let extension = parts.slice(-1)[0]
    return Object.keys(languages).includes(extension)
        ? languages[extension]
        : extension
}
