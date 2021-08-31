<script lang="ts">
	import { Router, Route } from "svelte-navigator";

	import Dashboard from './routes/Dashboard.svelte';
	import Account from './routes/Account.svelte';
	import MainNav from "./components/MainNav.svelte";
</script>

<main class="flex flex-col v-screen h-screen">
	<Router basepath="/app">
		<MainNav/>
		<div class="flex-1 overflow-auto px-4 py-4">
			<Route path="/"><Dashboard/></Route>
			<Route path="/account"><Account/></Route>
		</div>
	</Router>
</main>

<style global lang="postcss">
	@tailwind base;
	@tailwind components;
	@tailwind utilities;
</style>
