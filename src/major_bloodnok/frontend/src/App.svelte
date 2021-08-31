<script lang="ts">
	import { Router, Route } from "svelte-navigator";

	import Dashboard from './routes/Dashboard.svelte';
	import Account from './routes/Account.svelte';
	import MainNav from "./components/MainNav.svelte";
</script>

<main class="flex flex-col v-screen h-screen">
	<Router basepath="/app">
		<MainNav/>
		<Route path="/"><Dashboard/></Route>
		<Route path="/account/*"><Account/></Route>
	</Router>
</main>

<style global lang="postcss">
	@tailwind base;
	@tailwind components;
	@tailwind utilities;
</style>
