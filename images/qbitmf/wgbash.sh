#!/bin/bash

# Simple convenience script to run bash within the wg netns.

exec ip netns exec wg bash
