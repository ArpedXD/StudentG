const wait = (ms) => new Promise(resolve => setTimeout(resolve, ms));
const $ = (id) => document.getElementById(id)