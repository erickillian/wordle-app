<template>
    <v-app id="app">
        <navbar />
        <v-main>
            <router-view /> 
        </v-main>
    </v-app>
</template>

<script>
import Navbar from "@/components/Navbar";

export default {
    name: "main-layout",
    components: { Navbar },
    data() {
        return {}
    }
};
</script>
