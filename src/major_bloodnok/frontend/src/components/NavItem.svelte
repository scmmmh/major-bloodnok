<script lang="ts">
	import { link, useResolve } from "svelte-navigator";

    let cls = '';
    export { cls as class };
    const resolve = useResolve();
    export let href: string;
</script>

<li>
    <a href={resolve(href)} use:link class="block {cls}"><slot></slot></a>
</li>
