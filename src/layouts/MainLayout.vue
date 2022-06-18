<template>
    <v-app id="app">
        <NavbarComponent />
        <v-main>
            <router-view /> 
        </v-main>
    </v-app>
</template>

<script>
import NavbarComponent from "@/components/NavbarComponent";

export default {
    name: "main-layout",
    components: { NavbarComponent },
    data() {
        return {}
    }
};
</script>
