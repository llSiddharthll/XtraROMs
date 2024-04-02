import React from 'react';
import type {Meta, StoryObj} from '@storybook/react';

import {theme} from './theme';

const meta: Meta<typeof theme> = {
  component: theme,
};

export default meta;

type Story = StoryObj<typeof theme>;

export const Basic: Story = {args: {}};
