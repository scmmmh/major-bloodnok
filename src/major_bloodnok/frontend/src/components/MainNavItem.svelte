<script lang="ts">
	import { useLocation, link, useResolve } from "svelte-navigator";

    const resolve = useResolve();
    const location = useLocation();
    export let href: string;
    export let exact = true;
    let resolvedHref: string;
    let isCurrent: boolean;

    $: {
        resolvedHref = resolve(href);
        if (exact) {
            isCurrent = $location.pathname === href;
        } else {
            isCurrent = $location.pathname.startsWith(href);
        }
    }
</script>

<li>
    <a href={resolvedHref} use:link class="block px-4 py-2 {isCurrent ? 'bg-white text-blue-800' : 'bg-blue-800 text-white'} border-t-2 border-blue-800"><slot></slot></a>
</li>
