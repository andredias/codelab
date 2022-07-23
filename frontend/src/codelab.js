import axios from 'axios'


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
