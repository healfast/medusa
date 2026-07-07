const output = document.getElementById('demo-output');
const form = document.getElementById('demo-form');
const input = document.getElementById('demo-input');

function classifyIntent(prompt) {
  const text = (prompt || '').toLowerCase();
  if (/(plan|steps|roadmap|todo|project)/.test(text)) return 'planning';
  if (/(code|implement|build|debug|fix|write)/.test(text)) return 'coding';
  if (/(explain|what is|why|how)/.test(text)) return 'explanation';
  return 'chat';
}

function fallbackReply(prompt) {
  const text = prompt.toLowerCase();
  const intent = classifyIntent(prompt);

  if (intent === 'planning') {
    return "A strong plan starts with the goal, the milestones, and the first small step. I can help you structure the work clearly and keep it moving.";
  }
  if (intent === 'coding') {
    return "The fastest path is to start with the core behavior, add tests, and iterate until the result is reliable and maintainable.";
  }
  if (intent === 'explanation') {
    return "A concise explanation usually works best: define the idea, give a concrete example, and highlight the tradeoffs so it is easy to apply.";
  }
  if (/(file|repo|project|function|class|module)/.test(text)) {
    return "I can help inspect repository files, summarize structure, and point to the best next change with a practical focus.";
  }
  return "I can help you plan work, write code, explain concepts, and keep the process calm and practical.";
}

async function buildReply(prompt) {
  const endpoint = window.MEDUSA_AGENT_ENDPOINT || (window.location.hostname === 'localhost' ? '/api/chat' : null);

  if (endpoint) {
    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: prompt, provider: 'local', jailbreak: true }),
      });
      if (response.ok) {
        const data = await response.json();
        if (data && data.reply) {
          return data.reply;
        }
      }
    } catch (error) {
      console.warn('Falling back to local preview logic:', error);
    }
  }

  return fallbackReply(prompt);
}

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const prompt = input.value.trim();
  if (!prompt) return;
  output.textContent = `You: ${prompt}`;
  output.classList.add('is-thinking');
  input.value = '';
  const reply = await buildReply(prompt);
  output.classList.remove('is-thinking');
  output.textContent = `Medusa: ${reply}`;
});
