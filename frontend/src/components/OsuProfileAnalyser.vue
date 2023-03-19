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
  export default {
    data() {
      return {
        profileUrl: "",
      };
    },
    methods: {
      analyseProfile() {
        alert(this.profileUrl);
        // Here you can call your backend API to analyze the profile using the profileUrl
        // You can use the axios library to make the API request
        // Example:
        // axios.post('/api/analyse-profile', { profileUrl: this.profileUrl })
        //   .then(response => {
        //     // Handle the response from the API
        //   })
        //   .catch(error => {
        //     // Handle the error from the API
        //   });
      },
    },
  };
  </script>

  