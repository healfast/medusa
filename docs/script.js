const output = document.getElementById('demo-output');
const form = document.getElementById('demo-form');
const input = document.getElementById('demo-input');

function buildReply(prompt) {
  const text = prompt.toLowerCase();
  if (/(plan|roadmap|steps|todo)/.test(text)) {
    return "A strong plan starts with the goal, the milestones, and the first small step. I can help you structure the work clearly and keep it moving.";
  }
  if (/(code|build|implement|debug|fix)/.test(text)) {
    return "The fastest path is to start with the core behavior, add tests, and iterate until the result is reliable and maintainable.";
  }
  if (/(what|why|how|explain)/.test(text)) {
    return "A concise explanation usually works best: define the idea, give a concrete example, and highlight the tradeoffs so it is easy to apply.";
  }
  if (/(file|repo|project)/.test(text)) {
    return "I can help inspect repository files, summarize structure, and point to the best next change with a practical focus.";
  }
  return "I can help you plan work, write code, explain concepts, and keep the process calm and practical.";
}

form.addEventListener('submit', (event) => {
  event.preventDefault();
  const prompt = input.value.trim();
  if (!prompt) return;
  output.textContent = `You: ${prompt}`;
  window.setTimeout(() => {
    output.textContent = `Medusa: ${buildReply(prompt)}`;
  }, 220);
  input.value = '';
});
