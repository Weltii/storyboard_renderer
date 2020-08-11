import Axios from "axios";

import axios from "axios";

export namespace BackendService {
  const protocol = "http://";
  const ip = "localhost";
  const port = "8000";
  const baseUrl = `${protocol}${ip}:${port}/`;

  export async function getCurrentProject() {
    const url = `${baseUrl}project/current/`;
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
    const url = `${baseUrl}project/${path}/`;
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
    const url = `${baseUrl}project/${path}/`;
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

  export async function saveStoryboard(storyboard: any) {
    const url = `${baseUrl}project/current/storyboard/`;
    let response = await axios
      .patch(url, storyboard)
      .then((response) => {
        return response;
      })
      .catch((reason) => {
        return reason.response;
      });
    return response;
  }

  export async function getAllLayouts() {
    const url = `${baseUrl}layouts/`;
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

  export async function getLayoutInformation(layoutName: string) {
    const url = `${baseUrl}layouts/${layoutName}/`;
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

  export async function renderProject() {
    const url = `${baseUrl}render_project/current/`;
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

  export async function getBase64Pdf(path: string) {
    const url = `${baseUrl}pdf/current/pdf/${path}/`;
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
}
