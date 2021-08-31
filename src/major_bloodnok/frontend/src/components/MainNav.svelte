<script lang="ts">
    import MainNavItem from './MainNavItem.svelte';
</script>

<nav class="bg-blue-800 px-4">
    <ul class="flex flex-row">
        <MainNavItem href="/">Dashboard</MainNavItem>
        <MainNavItem href="/account">Account</MainNavItem>
    </ul>
</nav>
