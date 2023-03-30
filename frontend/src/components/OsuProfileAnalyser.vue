<template>
  <div class="landing">
    <div class="content text-center text-uppercase text-light vertical-align: middle;">
      <h1 class="logo-text">Osu! Profile Analyser</h1>
      <div class="box">
        <table class="elementsContainer">
          <tr>
            <td>
              <input type="url" v-model="userId" placeholder="osu! profile url..." class="search">
            </td>
          </tr>
        </table>
      </div>
      <div class="container-search-btn">
        <button @click="getProfileStats(userId)" class="search-btn">Analyse profile</button>
      </div>
    </div>
    <div id="stats" v-if="stats" style="position: absolute; top: 100%; left: 0; width: 100%;">
      <Stats :stats="stats" />
    </div>
  </div>
</template>

  
  <script>
  import axios from 'axios'
  import Stats from "@/components/Stats.vue";

  export default {
    name: "OsuProfileAnalyser",
    components: {
    Stats
  },
    data() {
      return {
        userId: "",
        stats: null
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
      async getProfileStats(userId) {
    this.stats = null;
    const url = `http://localhost:8000/api/user/${userId}`;
    const response = await axios.get(url, {
      headers: {
        Authorization: `Bearer ${this.accessToken}`
      }
    });
    this.stats = response.data;
  },
  },
  };
  </script>

  