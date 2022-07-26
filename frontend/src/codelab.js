import axios from 'axios'
import md5 from 'crypto-js/md5'
import Base64 from 'crypto-js/enc-base64'

export async function get_project(project_id) {
    // check local storage for project first
    let project = localStorage.getItem(project_id)
    if (project) {
        return JSON.parse(project)
    }

    // if not, fetch from server
    let response = await axios.get(`${import.meta.env.VITE_API_URL}/playgrounds/${project_id}`)
    project = response.data

    // save to local storage
    localStorage.setItem(project_id, JSON.stringify(project))
    return project
}


function calc_id(json) {
    // uses the same calculation as the server
    let str_hash = md5(JSON.stringify(json))
    return Base64.stringify(str_hash)
        .replace(/\+/g, '-') // Convert '+' to '-'
        .replace(/\//g, '_') // Convert '/' to '_'
        .replace(/=+$/, '') // Remove ending '='
}


export async function run_project(language, sourcecode, stdin) {
    let project_input = { language, sourcecode, stdin }

    // check local cache for project
    let project_id = calc_id(project_input)
    let project = localStorage.getItem(project_id)
    if (project) {
        console.debug('Local cache hit for project ' + project_id)
        return JSON.parse(project)
    }

    // not cached, fetch from server
    console.debug('Local cache miss for project ' + project_id)
    let response = await axios.post(`${import.meta.env.VITE_API_URL}/playgrounds`, {
        language,
        sourcecode,
        stdin,
    })
    project = { ...project_input, ...response.data }

    // save to local storage
    localStorage.setItem(project.id, JSON.stringify(project))

    return project
}


export async function load_examples() {
    let examples = localStorage.getItem('examples')
    if (examples) {
        return JSON.parse(examples)
    }
    let response = await axios.get(`${import.meta.env.VITE_API_URL}/examples`)
    examples = response.data
    // para cada exemplo, registrar no local storage
    // adicionar exemplo_id e título em hashmap da linguagem
    let current_language = null
    let language_examples = {}
    for (let example of examples) {
        if (current_language !== example.language) {
            current_language = example.language
            language_examples[current_language] = []
        }
        language_examples[current_language].push({
            id: example.id,
            title: example.title,
        })
        localStorage.setItem(example.id, JSON.stringify(example))
    }
    localStorage.setItem('examples', JSON.stringify(language_examples))
    return language_examples
}
