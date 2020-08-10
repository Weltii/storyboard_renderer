import Axios from "axios";

import axios from "axios";

export namespace BackendService {
  const protocol = "http://";
  const ip = "localhost";
  const port = "8000";
  const baseUrl = `${protocol}${ip}:${port}/`;

  export async function getCurrentProject() {
    const url = `${baseUrl}project/current`;
    let response = await axios
      .get(url)
      .then((response) => {
        return response;
      })
      .catch((reason) => {
        return reason.response;
      });
    return response;
  }

  export async function getProject(path: string) {
    const url = `${baseUrl}project/${path}`;
    let response = await axios
      .get(url)
      .then((response) => {
        return response;
      })
      .catch((reason) => {
        return reason.response;
      });
    return response;
  }

  export async function createProject(path: string) {
    const url = `${baseUrl}project/${path}`;
    let response = await axios
      .post(url)
      .then((response) => {
        return response;
      })
      .catch((reason) => {
        return reason.response;
      });
    return response;
  }

  export async function closeProject() {
    const url = `${baseUrl}project/close/current/`;
    let response = await axios
      .patch(url)
      .then((response) => {
        return response;
      })
      .catch((reason) => {
        return reason.response;
      });
    return response;
  }
}
