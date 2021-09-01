<script lang="ts">
	import { useLocation, link } from "svelte-navigator";

    import NavItem from './NavItem.svelte';

    const location = useLocation();
    export let href: string;
    export let exact = true;
    let resolvedHref: string;
    let isCurrent: boolean;

    $: {
        if (exact) {
            isCurrent = $location.pathname === href;
        } else {
            isCurrent = $location.pathname.startsWith(href);
        }
    }
</script>

<li>
    <NavItem href={href} class="px-4 py-2 {isCurrent ? 'bg-white text-blue-800' : 'bg-blue-800 text-white'} border-t-2 border-blue-800"><slot></slot></NavItem>
</li>
