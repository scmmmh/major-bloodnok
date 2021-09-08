<script lang="ts">
    import MainNavItem from './MainNavItem.svelte';
</script>

<nav class="flex-0 bg-blue-800 px-4">
    <ul class="flex flex-row">
        <MainNavItem href="/">Dashboard</MainNavItem>
        <MainNavItem href="/account" exact={false}>Account</MainNavItem>
        <MainNavItem href="/categories">Categories</MainNavItem>
    </ul>
</nav>
