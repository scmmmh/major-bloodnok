<script lang="ts">
	import { useNavigate, useLocation } from "svelte-navigator";

    const navigate = useNavigate();
    const location = useLocation();
    export let href: string;

    function clickHandler(ev: MouseEvent) {
        ev.preventDefault();
        if (ev.target) {
            navigate((ev.target as HTMLElement).getAttribute('href'));
        }
    }
</script>

<li>
    <a href={href} on:click={clickHandler} class="block px-4 py-2 {$location.pathname === href ? 'bg-white text-blue-800' : 'bg-blue-800 text-white'} border-t-2 border-blue-800"><slot></slot></a>
</li>
