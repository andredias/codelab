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
    localStorage.clear()
    let response = await axios.get(`${import.meta.env.VITE_API_URL}/examples`)
    let examples = response.data
    localStorage.setItem('examples', JSON.stringify(examples))
    const languages = new Set()
    for (let example of examples) {
        localStorage.setItem(example.id, JSON.stringify(example))
        languages.add(example.language)
    }
    localStorage.setItem('languages', JSON.stringify([...languages]))
    return examples
}
