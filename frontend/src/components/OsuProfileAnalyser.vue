<template>
    <div class="landing">
      <div class="content text-center text-uppercase text-light vertical-align: middle;">
        <h1 class="logo-text">Osu! Profile Analyser</h1>
        <div class="box">
          <table class="elementsContainer">
            <tr>
              <td>
                <input type="url" v-model="profileUrl" placeholder="osu! profile url..." class="search">
              </td>
            </tr>
          </table>
        </div>
        <div class="container-search-btn">
          <button @click="analyseProfile" class="search-btn">Analyse profile</button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios'

  export default {
    data() {
      return {
        profileUrl: "",
      };
    },
    mounted() {
    axios.get('http://localhost:8000/api/validate_token')
      .then(response => {
        // handle successful response
        console.log(response.data)
      })
      .catch(error => {
        // handle error
        console.log(error)
      })
  },
    methods: {
        async analyseProfile() {
    const response = await fetch(`http://localhost:8000/parse_url?url=${this.profileUrl}`);
    const data = await response.json();
    if (data && data.name) {
      alert(`User name: ${data.name}`);
    } else {
      alert('Could not parse user name from the provided URL');
    }
  },
    },
  };
  </script>

  